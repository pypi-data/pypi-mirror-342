import base64
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, Union
from urllib import parse
from urllib.request import Request, HTTPError, urlopen

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from .entities import *

logger = logging.getLogger('gsalary-cli')

__all__ = ['GSalaryClient', 'GSalaryException', 'GSalaryRequest', ]


def url_encode(args: Dict[str, str], escape: bool = False) -> str:
    return '&'.join([f'{k}={v if not escape else parse.quote(v)}' for k, v in args.items()])


def _generate_rsa_signature(private_key, sign_base):
    try:
        signature = private_key.sign(
            sign_base.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    except Exception as e:
        logger.error(f'Generate signature error: {e}')
        raise ValueError('Failed to generate RSA signature') from e


class GSalaryException(Exception):
    _biz_code = None
    _error_code = None
    _message = None

    def __init__(self, biz_code, error_code, message):
        self._biz_code = biz_code
        self._error_code = error_code
        self._message = message

    @property
    def biz_code(self):
        return self._biz_code

    @property
    def error_code(self):
        return self._error_code

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f'[{self._biz_code} - {self._error_code}] {self._message}'


class GSalaryRequest:
    _method = None
    _path = None
    _query_args: Dict[str, str] = None
    _body: Dict = None

    def __init__(self, method: str, path: str,
                 query_args: Union[None, Dict[str, str]] = None,
                 body: Union[None, Dict] = None):
        self._method = method
        self._path = path
        self._query_args = query_args
        self._body = body
        self.valid()

    def valid(self):
        if not self._method or not self._path:
            raise ValueError('Invalid request')
        if self._method not in ['GET', 'PUT', 'POST', 'DELETE']:
            raise ValueError('Invalid method')

    def has_body(self):
        if self._method in ['PUT', 'POST']:
            return self._body is not None
        return False

    @property
    def method(self):
        return self._method

    def path_with_args(self, escape: bool = False):
        if self._query_args is None or len(self._query_args) == 0:
            return self._path
        return self._path + '?' + url_encode(self._query_args, escape)

    def _get_body_hash(self):
        if self._body:
            body_str = json.dumps(self._body)
            hash_bytes = hashlib.sha256(body_str.encode('utf-8')).digest()
            return base64.b64encode(hash_bytes).decode('utf-8')
        return ''

    def sign_request(self, config: GSalaryConfig):
        timestamp = str(int(datetime.now().timestamp() * 1000))
        sign_base = f'{self.method} {self.path_with_args(False)}\n{config.appid}\n{timestamp}\n{self._get_body_hash()}\n'
        logger.debug(f'sign base for signature: {sign_base}')
        sign = _generate_rsa_signature(config.client_private_key, sign_base)
        return AuthoriseHeaderInfo(
            algorithm='RSA2',
            timestamp=timestamp,
            signature=sign
        )

    def verify_signature(self, config: GSalaryConfig, header_info: AuthoriseHeaderInfo, body: str):
        body_hash = base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode('utf-8')
        sign_base = f'{self.method} {self.path_with_args(False)}\n{config.appid}\n{header_info.timestamp}\n{body_hash}\n'
        logger.debug(f'sign base for verify: {sign_base}')
        try:
            public_key = config.server_public_key
            signature = base64.b64decode(header_info.signature)
            public_key.verify(
                signature,
                sign_base.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            logger.error(f'Verify signature error: {e}')
            return False

    @property
    def body(self):
        return self._body


class GSalaryClient:
    _config: GSalaryConfig = None

    def __init__(self, config: GSalaryConfig):
        self._config = config

    def request(self, request: GSalaryRequest) -> Dict:

        _headers = {
            'X-Appid': self._config.appid,
            'Content-Type': 'application/json',
            'Authorization': request.sign_request(self._config).to_header_value()
        }
        _http_req = Request(
            url=self._config.concat_path(request.path_with_args(True)),
            method=request.method,
            data=json.dumps(request.body).encode('utf-8') if request.has_body() else None,
            headers=_headers
        )
        logger.debug(f'submitting gsalary request {request.method} to {_http_req.full_url}')
        try:
            with urlopen(_http_req) as response:
                response_data = response.read().decode('utf-8')
                logger.debug(f'gsalary response: {response_data}')
                if response.status == 200:
                    auth_header = from_header_value(response.headers['Authorization'])
                    if not auth_header.valid():
                        logger.error('Invalid authorization header')
                        raise ValueError('Invalid authorization header')
                    verified = request.verify_signature(self._config,
                                                        auth_header,
                                                        response_data)
                    if not verified:
                        logger.error('Signature verification failed')
                        raise ValueError('Signature verification failed')
                    try:
                        return json.loads(response_data)
                    except json.JSONDecodeError:
                        logger.error(f'Non-JSON response: {response_data}')
                        raise ValueError(f'Unexpected response format: {response_data}')
                else:
                    try:
                        body = json.loads(response_data)
                        raise GSalaryException(body.get('biz_result'), body.get('error_code'), body.get('message'))
                    except json.JSONDecodeError:
                        logger.error(f'Non-JSON response: {response_data}')
                        raise ValueError(f'Unexpected response format: {response_data}')
        except HTTPError as e:
            try:
                err_content = e.read().decode('utf-8')
                logger.error(f'gsalary response error {e.status}: {err_content}')
                body = json.loads(err_content)
                raise GSalaryException(body.get('biz_result'), body.get('error_code'), body.get('message'))
            except Exception as e2:
                logger.error(f'HTTPError: {e}')
                raise e

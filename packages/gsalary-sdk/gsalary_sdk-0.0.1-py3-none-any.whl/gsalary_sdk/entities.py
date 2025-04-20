from urllib import parse
from cryptography.hazmat.primitives import serialization

__all__ = ["GSalaryConfig", "AuthoriseHeaderInfo", "from_header_value"]


class GSalaryConfig:
    endpoint: str = 'https://api-test.gsalary.com'
    appid: str = None
    _client_private_key = None
    _server_public_key = None

    def concat_path(self, path):
        if path.startswith('/'):
            path = path[1:]
        if self.endpoint.endswith('/'):
            return self.endpoint + path
        else:
            return self.endpoint + '/' + path

    @property
    def client_private_key(self):
        return self._client_private_key

    @property
    def server_public_key(self):
        return self._server_public_key

    @staticmethod
    def _insert_new_lines(value: str) -> str:
        value = value.strip()
        # 去除已有的头尾
        if value.startswith('-----BEGIN PUBLIC KEY-----'):
            value = value[len('-----BEGIN PUBLIC KEY-----'):].strip()
        if value.endswith('-----END PUBLIC KEY-----'):
            value = value[:-len('-----END PUBLIC KEY-----')].strip()
        # 按每 64 个字符插入一个换行符
        return '\n'.join(value[i:i + 64] for i in range(0, len(value), 64))

    def config_client_private_key_pem(self, value: str):
        if not value.startswith('-----BEGIN PRIVATE KEY-----'):
            if value.strip().count('\n') <= 0:
                value = self._insert_new_lines(value)
            value = '-----BEGIN PRIVATE KEY-----\n' + value + '\n-----END PRIVATE KEY-----'
        print('loaded private key:' + value)
        self._client_private_key = serialization.load_pem_private_key(value.encode(), password=None)

    def config_client_private_key_pem_file(self, value: str):
        with open(value, 'r') as f:
            content = f.read()
            self.config_client_private_key_pem(content)

    def config_server_public_key_pem(self, value: str):
        if not value.startswith('-----BEGIN PUBLIC KEY-----'):
            if value.strip().count('\n') <= 0:
                value = self._insert_new_lines(value)
            value = '-----BEGIN PUBLIC KEY-----\n' + value + '\n-----END PUBLIC KEY-----'
        print('loaded public key:' + value)
        self._server_public_key = serialization.load_pem_public_key(value.encode())

    def config_server_public_key_pem_file(self, value: str):
        with open(value, 'r') as f:
            content = f.read()
            self.config_server_public_key_pem(content)


class AuthoriseHeaderInfo:
    _algorithm = None
    _timestamp = None
    _signature = None

    def __init__(self, algorithm, timestamp, signature):
        self._algorithm = algorithm
        self._timestamp = timestamp
        self._signature = signature

    @property
    def valid(self):
        return self._algorithm is not None and self._timestamp is not None and self._signature is not None

    def to_header_value(self):
        return "algorithm={},time={},signature={}".format(self._algorithm, self._timestamp,
                                                          parse.quote(self._signature))

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def signature(self):
        return self._signature


def from_header_value(header_value) -> AuthoriseHeaderInfo:
    if header_value is None:
        return AuthoriseHeaderInfo(None, None, None)
    parts = header_value.split(",")
    if len(parts) != 3:
        return AuthoriseHeaderInfo(None, None, None)
    # 拆分提取key=value，根据key的值进行提取
    algorithm = None
    timestamp = None
    signature = None
    for part in parts:
        key_value = part.split("=")
        if len(key_value) != 2:
            continue
        key = key_value[0]
        value = key_value[1]
        if key == "algorithm":
            algorithm = value
        elif key == "time":
            timestamp = value
        elif key == "signature":
            signature = parse.unquote(value)
    return AuthoriseHeaderInfo(algorithm, timestamp, signature)

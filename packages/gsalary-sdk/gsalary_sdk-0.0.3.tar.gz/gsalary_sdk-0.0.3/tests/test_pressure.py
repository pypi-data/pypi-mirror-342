import json
import logging
from gsalary_sdk import GSalaryClient, GSalaryConfig, GSalaryRequest
from datetime import datetime
import random

# init logger to print on console
logger = logging.getLogger('gsalary-cli')
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def submit_new_transfer(cli: GSalaryClient, order_id: str, quote_id: str):
    submit_body = {
        "quote_id": quote_id,
        "client_order_id": order_id
    }
    submit_req = GSalaryRequest('POST', '/v1/remittance/orders', body=submit_body)
    try:
        resp = cli.request(submit_req)
    except any as e:
        return 'SUBMIT_FAIL'
    else:
        return 'PASSED'


def test_new_transfer(cli: GSalaryClient, order_id: str):
    quote_body = {
        "payee_account_id": "2025031109420476969800268761",
        "payer_id": "2025041503002236227200461571",
        "purpose": "SALARY",
        "pay_currency": "USD",
        "receive_currency": "USD",
        "amount": 10,
        "amount_type": "PAY_AMOUNT",
        "remark": "test"
    }
    req = GSalaryRequest('POST', '/v1/remittance/quotes', body=quote_body)
    try:
        resp = cli.request(req)
    except BaseException as e:
        logger.error(f'quote failed: {e}', exc_info=True)
        return 'QUOTE_FAIL'
    else:
        quote_data = resp.get('data')
        return submit_new_transfer(cli, order_id, quote_data.get('quote_id'))


def test_single(cli: GSalaryClient):
    order_id = 'test_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(random.randint(100000, 999999))
    std = test_new_transfer(cli, order_id)
    logger.info(f'submitted order {order_id} std: {std}')


if __name__ == '__main__':
    # load config from os environment args
    config = GSalaryConfig()
    config.endpoint = 'http://gsalary-api.dev.geekforbest.com'
    config.appid = '2024040810211195494000456601'
    config.config_client_private_key_pem_file('D:\\AstroDocuments\\certs\\gsalary\\eason-test\\client-priv.pem')
    config.config_server_public_key_pem_file('D:\\AstroDocuments\\certs\\gsalary\\eason-test\\server-pub.pem')
    _cli = GSalaryClient(config)
    test_single(_cli)

import json
import logging
from src.gsalary_sdk import GSalaryClient, GSalaryConfig, GSalaryRequest
import os

# init logger to print on console
logger = logging.getLogger('gsalary-cli')
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def test_list_cards(cli: GSalaryClient):
    req = GSalaryRequest('GET', '/v1/cards', query_args={'page': '1', 'limit': '20'})
    resp = cli.request(req)
    print(json.dumps(resp, indent=4))


if __name__ == '__main__':
    # load config from os environment args
    config = GSalaryConfig()
    config.appid = os.environ.get('GSALARY_APPID')
    config.config_client_private_key_pem_file(os.environ.get('GSALARY_CLIENT_PRIVATE_KEY_PEM_FILE'))
    config.config_server_public_key_pem_file(os.environ.get('GSALARY_SERVER_PUBLIC_KEY_PEM_FILE'))
    _cli = GSalaryClient(config)
    test_list_cards(_cli)

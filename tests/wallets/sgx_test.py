import mock
import web3

from hexbytes import HexBytes
from eth_account.datastructures import AttributeDict
from skale.wallets import SgxWallet
from skale.utils.web3_utils import (
    init_web3,
    private_key_to_address,
    to_checksum_address
)

from tests.constants import ENDPOINT, ETH_PRIVATE_KEY

ADDRESS = to_checksum_address(
    private_key_to_address(ETH_PRIVATE_KEY)
)


class SgxClient:
    def __init__(self, endpoint, path_to_cert=None):
        pass

    def generate_key(self):
        return AttributeDict({
            'name': 'NEK:aaabbb',
            'address': ADDRESS,
            'public_key': 'ab00000000000000000000000000000000000000',
        })

    def get_account(self, key_name):
        return AttributeDict({
            'address': ADDRESS,
            'public_key': 'ab00000000000000000000000000000000000000',
        })

    def sign(self, transaction_dict, key_name):
        return AttributeDict({
            'rawTransaction': HexBytes('0x000000000000'),
            'hash': HexBytes('0x000000000000'),
            'r': 100000000000,
            's': 100000000000,
            'v': 37,
        })

    def sign_hash(self, message, key_name, chain_id):
        return AttributeDict({
            'messageHash': HexBytes('0x0'),
            'r': 123,
            's': 123,
            'v': 27,
            'signature': HexBytes('0x0')
        })


def test_sgx_sign():
    with mock.patch('skale.wallets.sgx_wallet.SgxClient',
                    new=SgxClient):
        web3 = init_web3(ENDPOINT)
        wallet = SgxWallet('TEST_ENDPOINT', web3)
        tx_dict = {
            'to': '0x1057dc7277a319927D3eB43e05680B75a00eb5f4',
            'value': 9,
            'gas': 200000,
            'gasPrice': 1,
            'nonce': 7,
            'chainId': None,
            'data': b'\x9b\xd9\xbb\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x95qY\xc4i\xfc;\xba\xa8\xe3\x9e\xe0\xa3$\xc28\x8a\xd6Q\xe5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\xe0\xb6\xb3\xa7d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x006\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa8\xc0\x04/Rglamorous-kitalpha\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # noqa
        }
        wallet.sign(tx_dict)


def test_sgx_sign_without_nonce():
    with mock.patch('skale.wallets.sgx_wallet.SgxClient',
                    new=SgxClient):
        web3 = init_web3(ENDPOINT)
        wallet = SgxWallet('TEST_ENDPOINT', web3)
        tx_dict = {
            'to': '0x1057dc7277a319927D3eB43e05680B75a00eb5f4',
            'value': 9,
            'gas': 200000,
            'gasPrice': 1,
            'chainId': None,
            'data': b'\x9b\xd9\xbb\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x95qY\xc4i\xfc;\xba\xa8\xe3\x9e\xe0\xa3$\xc28\x8a\xd6Q\xe5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\xe0\xb6\xb3\xa7d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x006\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa8\xc0\x04/Rglamorous-kitalpha\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # noqa
        }
        wallet.sign(tx_dict)


def test_sgx_sign_and_send_without_nonce():
    with mock.patch.object(web3.eth.Eth, 'sendRawTransaction') as send_tx_mock:
        with mock.patch('skale.wallets.sgx_wallet.SgxClient',
                        new=SgxClient):
            web3_inst = init_web3(ENDPOINT)
            wallet = SgxWallet('TEST_ENDPOINT', web3_inst)
            tx_dict = {
                'to': '0x1057dc7277a319927D3eB43e05680B75a00eb5f4',
                'value': 9,
                'gas': 200000,
                'gasPrice': 1,
                'chainId': None,
                'data': b'\x9b\xd9\xbb\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x95qY\xc4i\xfc;\xba\xa8\xe3\x9e\xe0\xa3$\xc28\x8a\xd6Q\xe5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\xe0\xb6\xb3\xa7d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x006\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa8\xc0\x04/Rglamorous-kitalpha\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # noqa
            }
            signed = wallet.sign(tx_dict)
            wallet.sign_and_send(tx_dict)
            send_tx_mock.assert_called_with(signed.rawTransaction)


def test_sgx_sign_with_key():
    with mock.patch('skale.wallets.sgx_wallet.SgxClient',
                    new=SgxClient):
        web3 = init_web3(ENDPOINT)
        wallet = SgxWallet('TEST_ENDPOINT', web3, key_name='TEST_KEY')
        tx_dict = {
            'to': '0x1057dc7277a319927D3eB43e05680B75a00eb5f4',
            'value': 10,
            'gas': 200000,
            'gasPrice': 1,
            'nonce': 7,
            'chainId': None,
            'data': b'\x9b\xd9\xbb\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x95qY\xc4i\xfc;\xba\xa8\xe3\x9e\xe0\xa3$\xc28\x8a\xd6Q\xe5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\xe0\xb6\xb3\xa7d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x006\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa8\xc0\x04/Rglamorous-kitalpha\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # noqa
        }
        wallet.sign(tx_dict)


def test_sgx_sign_hash():
    with mock.patch('skale.wallets.sgx_wallet.SgxClient',
                    new=SgxClient):
        web3 = init_web3(ENDPOINT)
        wallet = SgxWallet('TEST_ENDPOINT', web3, key_name='TEST_KEY')
        unsigned_hash = '0x0'
        signed_message = wallet.sign_hash(unsigned_hash)
        assert signed_message.signature == HexBytes('0x0')


def test_sgx_key_init():
    with mock.patch('skale.wallets.sgx_wallet.SgxClient',
                    new=SgxClient):
        web3 = init_web3(ENDPOINT)
        wallet = SgxWallet('TEST_ENDPOINT', web3, 'TEST_KEY')
        assert wallet.key_name == 'TEST_KEY'
        assert wallet.address == ADDRESS
        assert wallet.public_key == 'ab00000000000000000000000000000000000000'

import sys

from skale import Skale
from skale.utils.account_tools import init_wallet
import skale.utils.helper as Helper

from examples.helper import ENDPOINT, LOCAL_ABI_FILEPATH

skale = Skale(ENDPOINT, LOCAL_ABI_FILEPATH)
#wallet = init_wallet()

if __name__ == "__main__":
    schain_name = sys.argv[1]

    wallet = {
        "address": "0x3C3B3E4E993dD6591d907ceAEDDa2731C83dB9F9",
        "private_key": "0x35c9a2598d912f0eb9daf3d5c8921e1740aaa334df5c0ac9585d5ad1a279101a"
    }
    res = skale.manager.delete_schain(schain_name, wallet)
    receipt = Helper.await_receipt(skale.web3, res['tx'])
    Helper.check_receipt(receipt)
    print(f'sChain {schain_name} removed!')

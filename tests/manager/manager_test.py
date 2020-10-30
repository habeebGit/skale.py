""" SKALE manager test """

import random

import mock
import pytest
import web3
from hexbytes import HexBytes
from mock import Mock

from skale.skale_manager import SkaleManager, spawn_skale_manager_from
from skale.transactions.exceptions import TransactionFailedError

from skale.utils.contracts_provision.main import (
    generate_random_node_data, generate_random_schain_data
)
from skale.utils.web3_utils import init_web3
from skale.wallets.web3_wallet import generate_wallet, Web3Wallet
from tests.constants import (
    ENDPOINT, ETH_PRIVATE_KEY, TEST_ABI_FILEPATH, TEST_GAS_LIMIT
)


def test_get_bounty(skale):
    node_id = 0
    nonce = skale.web3.eth.getTransactionCount(skale.wallet.address)
    contract_address = skale.manager.address
    chain_id = skale.web3.eth.chainId
    expected_txn = {
        'value': 0, 'gasPrice': skale.gas_price, 'chainId': chain_id,
        'gas': TEST_GAS_LIMIT, 'nonce': nonce,
        'to': contract_address,
        'data': (
            '0xee8c4bbf00000000000000000000000000000000000000000000'
            '00000000000000000000'
        )
    }
    exp = skale.web3.eth.account.signTransaction(
        expected_txn, skale.wallet._private_key).rawTransaction
    with mock.patch.object(skale.manager.contract.functions.getBounty, 'call',
                           new=Mock(return_value=[])):
        with mock.patch.object(web3.eth.Eth, 'sendRawTransaction') as send_tx_mock:
            send_tx_mock.return_value = b'hexstring'
            skale.manager.get_bounty(node_id, wait_for=False, gas_limit=TEST_GAS_LIMIT)
            send_tx_mock.assert_called_with(HexBytes(exp))


@pytest.mark.skip(reason="verdicts temporary disabled")
def test_send_verdict(skale):
    nonce = skale.web3.eth.getTransactionCount(skale.wallet.address)
    contract_address = skale.manager.address
    chain_id = skale.web3.eth.chainId
    expected_txn = {
        'value': 0, 'gasPrice': skale.gas_price, 'chainId': chain_id,
        'gas': 200000, 'nonce': nonce,
        'to': contract_address,
        'data': (
            '0x96a1ce46000000000000000000000000000000000000000'
            '0000000000000000000000000000000000000000000000000'
            '000000000000000000000000000000000000007b000000000'
            '0000000000000000000000000000000000000000000000000'
            '0000140000000000000000000000000000000000000000000'
            '00000000000000000000a'
        )
    }
    exp = skale.web3.eth.account.signTransaction(
        expected_txn, skale.wallet._private_key).rawTransaction
    validator_id = 0
    verdict_data = (123, 20, 10)
    with mock.patch.object(skale.manager.contract.functions.sendVerdict,
                           'call', new=Mock(return_value=[])):
        with mock.patch.object(web3.eth.Eth,
                               'sendRawTransaction') as send_tx_mock:
            send_tx_mock.return_value = b'hexstring'
            skale.manager.send_verdict(validator_id, verdict_data,
                                       wait_for=False)
            send_tx_mock.assert_called_with(HexBytes(exp))


@pytest.mark.skip(reason="verdicts temporary disabled")
def test_send_verdicts(skale):
    nonce = skale.web3.eth.getTransactionCount(skale.wallet.address)
    contract_address = skale.manager.address
    chain_id = skale.web3.eth.chainId
    expected_txn = {
        'value': 0, 'gasPrice': skale.gas_price, 'chainId': chain_id,
        'gas': 8000000, 'nonce': nonce,
        'to': contract_address,

        'data': (
            '0x42c81d610000000000000000000000000000000000000000'
            '00000000000000000000000000000000000000000000000000'
            '00000000000000000000000000000000000040000000000000'
            '00000000000000000000000000000000000000000000000000'
            '03000000000000000000000000000000000000000000000000'
            '000000000000007b0000000000000000000000000000000000'
            '00000000000000000000000000000100000000000000000000'
            '0000000000000000000000000000000000000000000a000000'
            '00000000000000000000000000000000000000000000000000'
            '000000e7000000000000000000000000000000000000000000'
            '00000000000000000000020000000000000000000000000000'
            '00000000000000000000000000000000001400000000000000'
            '000000000000000000000000000000000000000000000001c3'
            '000000000000000000000000000000000000000000000000000'
            '00000000000030000000000000000000000000000000000000'
            '00000000000000000000000001e')
    }
    exp = skale.web3.eth.account.signTransaction(
        expected_txn, skale.wallet._private_key).rawTransaction
    validator_id = 0
    verdicts_data = [(123, 1, 10), (231, 2, 20), (451, 3, 30)]
    with mock.patch.object(skale.manager.contract.functions.sendVerdicts,
                           'call', new=Mock(return_value=[])):
        with mock.patch.object(web3.eth.Eth,
                               'sendRawTransaction') as send_tx_mock:
            send_tx_mock.return_value = b'hexstring'
            skale.manager.send_verdicts(
                validator_id, verdicts_data,
                wait_for=False)
            send_tx_mock.assert_called_with(HexBytes(exp))


def test_create_delete_schain(skale):
    schains_ids = skale.schains_internal.get_all_schains_ids()

    type_of_nodes, lifetime_seconds, name = generate_random_schain_data()
    price_in_wei = skale.schains.get_schain_price(type_of_nodes,
                                                  lifetime_seconds)
    tx_res = skale.manager.create_schain(lifetime_seconds, type_of_nodes,
                                         price_in_wei, name, wait_for=True)
    assert tx_res.receipt['status'] == 1

    schains_ids_number_after = skale.schains_internal.get_schains_number()
    assert schains_ids_number_after == len(schains_ids) + 1
    schains_ids_after = skale.schains_internal.get_all_schains_ids()

    schains_names = [
        skale.schains.get(sid)['name']
        for sid in schains_ids_after
    ]
    assert name in schains_names

    tx_res = skale.manager.delete_schain(name, wait_for=True)
    assert tx_res.receipt['status'] == 1

    schains_ids_number_after = skale.schains_internal.get_schains_number()
    assert schains_ids_number_after == len(schains_ids)
    schains_ids_after = skale.schains_internal.get_all_schains_ids()

    schains_names = [
        skale.schains.get(sid)['name']
        for sid in schains_ids_after
    ]
    assert name not in schains_names


def test_create_delete_default_schain(skale):
    schains_ids = skale.schains_internal.get_all_schains_ids()
    name = ''.join(random.choice('abcde') for _ in range(4))
    tx_res = skale.manager.create_default_schain(name)
    assert tx_res.receipt['status'] == 1

    schains_ids_number_after = skale.schains_internal.get_schains_number()
    assert schains_ids_number_after == len(schains_ids) + 1
    schains_ids_after = skale.schains_internal.get_all_schains_ids()

    schains_names = [
        skale.schains.get(sid)['name']
        for sid in schains_ids_after
    ]
    assert name in schains_names

    tx_res = skale.manager.delete_schain(name, wait_for=True)
    assert tx_res.receipt['status'] == 1

    schains_ids_number_after = skale.schains_internal.get_schains_number()
    assert schains_ids_number_after == len(schains_ids)
    schains_ids_after = skale.schains_internal.get_all_schains_ids()

    schains_names = [
        skale.schains.get(sid)['name']
        for sid in schains_ids_after
    ]
    assert name not in schains_names


def test_create_node_status_0(patched_wallet_failed_tx_skale):
    skale = patched_wallet_failed_tx_skale
    ip, public_ip, port, name = generate_random_node_data()
    tx_res = skale.manager.create_node(ip, port, name,
                                       wait_for=True, raise_for_status=False)
    assert tx_res.receipt['status'] == 0
    with pytest.raises(TransactionFailedError):
        tx_res.raise_for_status()


def test_empty_node_exit(skale):
    ip, public_ip, port, name = generate_random_node_data()
    skale.manager.create_node(ip, port, name, public_ip, wait_for=True)
    node_idx = skale.nodes.node_name_to_index(name)
    tx_res = skale.manager.node_exit(node_idx, wait_for=True)
    assert tx_res.receipt['status'] == 1
    assert skale.nodes.get_node_status(node_idx) == 2


def test_failed_node_exit(skale):
    schains_ids = skale.schains_internal.get_all_schains_ids()
    schain_name = skale.schains.get(schains_ids[0])['name']
    exit_node_id = skale.schains_internal.get_node_ids_for_schain(schain_name)[0]
    with pytest.raises(TransactionFailedError):
        skale.manager.node_exit(exit_node_id, skip_dry_run=True,
                                wait_for=True, gas_limit=TEST_GAS_LIMIT)


def test_grant_role(skale):
    wallet = generate_wallet(skale.web3)
    default_admin_role = skale.manager.default_admin_role()
    assert not skale.manager.has_role(default_admin_role, wallet.address)

    skale.manager.grant_role(
        default_admin_role,
        wallet.address,
        wait_for=True
    )
    assert skale.manager.has_role(default_admin_role, wallet.address)


def test_grant_admin_role(skale):
    wallet = generate_wallet(skale.web3)
    admin_role = skale.manager.admin_role()
    assert not skale.manager.has_role(admin_role, wallet.address)

    skale.manager.grant_role(
        admin_role,
        wallet.address,
        wait_for=True
    )
    assert skale.manager.has_role(admin_role, wallet.address)


def test_spawn_skale_manager_from():
    web3 = init_web3(ENDPOINT)
    wallet = Web3Wallet(ETH_PRIVATE_KEY, web3)
    provider_timeout = 20
    manager = SkaleManager(ENDPOINT, TEST_ABI_FILEPATH, wallet,
                           provider_timeout=provider_timeout)
    new_manager = spawn_skale_manager_from(manager)
    assert manager.wallet is new_manager.wallet
    assert manager._provider_timeout == new_manager._provider_timeout
    lib_contracts = manager._SkaleBase__contracts
    new_lib_contracts = new_manager._SkaleBase__contracts
    assert len(lib_contracts) == len(new_lib_contracts)

    new_wallet = Web3Wallet(ETH_PRIVATE_KEY, web3)
    new_provider_timeout = 30
    new_manager = spawn_skale_manager_from(manager, wallet=new_wallet,
                                           provider_timeout=new_provider_timeout)

    assert new_manager.wallet is new_wallet
    assert new_manager._provider_timeout == new_provider_timeout

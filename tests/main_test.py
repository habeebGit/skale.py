#   -*- coding: utf-8 -*-
#
#   This file is part of SKALE.py
#
#   Copyright (C) 2019 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" SKALE main test """

from web3 import WebsocketProvider

from skale import BlockchainEnv, Skale
from skale.contracts import BaseContract
from skale.contracts.functionality.nodes import Nodes
from skale.contracts_info import CONTRACTS_INFO
from skale.utils.contract_info import ContractInfo
from tests.constants import TEST_CONTRACT_NAME, RPC_IP, RPC_PORT


def test_lib_init():
    skale = Skale(BlockchainEnv.TEST, ip=RPC_IP, ws_port=RPC_PORT)

    lib_contracts_info = skale._Skale__contracts_info
    for contract_info in CONTRACTS_INFO:
        assert isinstance(lib_contracts_info[contract_info.name], ContractInfo)

    lib_contracts = skale._Skale__contracts
    assert len(lib_contracts) == len(CONTRACTS_INFO)

    for contract_name in lib_contracts:
        lib_contract = lib_contracts[contract_name]
        assert issubclass(type(lib_contract), BaseContract)
        assert lib_contract.address is not None
        assert lib_contract.abi is not None

    assert skale.abi is not None

    provider = skale.web3.providers[0]
    assert isinstance(provider, WebsocketProvider)


def test_get_contract_address(skale):
    lib_nodes_functionality_address = skale.get_contract_address(TEST_CONTRACT_NAME)
    nodes_functionality_address = skale.nodes.address

    assert lib_nodes_functionality_address == nodes_functionality_address


def test_get_attr(skale):
    skale_py_nodes_contract = skale.nodes
    assert issubclass(type(skale_py_nodes_contract), BaseContract)
    assert isinstance(skale_py_nodes_contract, Nodes)

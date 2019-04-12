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
""" SKALE manager test """

import skale.utils.helper as Helper
from tests.constants import DEFAULT_NODE_ID
from tests.utils import generate_random_node_data, generate_random_schain_data


def test_create_node(skale, wallet):
    active_node_ips_before = skale.nodes_data.get_active_node_ips()

    ip, public_ip, port, name = generate_random_node_data()
    res = skale.manager.create_node(ip, port, name, wallet, public_ip)
    receipt = Helper.await_receipt(skale.web3, res['tx'])

    assert receipt['status'] == 1

    active_node_ips_after = skale.nodes_data.get_active_node_ips()
    assert len(active_node_ips_after) == len(active_node_ips_before) + 1


def test_create_node_data_to_bytes(skale, wallet):
    ip, public_ip, port, name = generate_random_node_data()
    skale_nonce = Helper.generate_nonce()
    pk = Helper.private_key_to_public(wallet['private_key'])

    bytes_data = skale.manager.create_node_data_to_bytes(ip, public_ip, port, name, pk, skale_nonce)
    name_bytes = name.encode()

    assert type(bytes_data) is bytes
    assert bytes_data.find(name_bytes) != -1


def test_create_schain(skale, wallet):
    type_of_nodes, lifetime_seconds, name = generate_random_schain_data()
    price_in_wei = skale.schains.get_schain_price(type_of_nodes, lifetime_seconds)
    res = skale.manager.create_schain(lifetime_seconds, type_of_nodes, price_in_wei, name, wallet)
    receipt = Helper.await_receipt(skale.web3, res['tx'])

    assert receipt['status'] == 1


def test_create_schain_data_to_bytes(skale):
    type_of_nodes, lifetime_seconds, name = generate_random_schain_data()
    skale_nonce = Helper.generate_nonce()

    bytes_data = skale.manager.create_schain_data_to_bytes(
        lifetime_seconds,
        type_of_nodes,
        name,
        skale_nonce
    )
    name_bytes = name.encode()

    assert type(bytes_data) is bytes
    assert bytes_data.find(name_bytes) != -1


def test_get_bounty(skale, wallet):
    res = skale.manager.get_bounty(DEFAULT_NODE_ID, wallet)
    receipt = Helper.await_receipt(skale.web3, res['tx'])
    print(receipt)
    # assert receipt['status'] == 1 # todo: we couldn't test it here
    # todo: check account balance before and after


def test_send_verdict(skale, wallet):
    pass  # todo!

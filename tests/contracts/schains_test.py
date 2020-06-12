""" SKALE chain test """

from skale.contracts.schains import FIELDS
from skale.utils.constants import SCHAIN_TYPES
from tests.constants import (DEFAULT_NODE_NAME, DEFAULT_SCHAIN_ID,
                             DEFAULT_SCHAIN_NAME, LIFETIME_SECONDS)


def test_get(skale):
    schain = skale.schains.get(DEFAULT_SCHAIN_ID)
    assert list(schain.keys()) == FIELDS
    assert [k for k, v in schain.items() if v is None] == []


def test_get_by_name(skale):
    schain = skale.schains.get(DEFAULT_SCHAIN_ID)
    schain_name = schain['name']

    schain_by_name = skale.schains.get_by_name(schain_name)
    assert list(schain_by_name.keys()) == FIELDS
    assert schain == schain_by_name


def test_get_schains_for_owner(skale, empty_account):
    schains = skale.schains.get_schains_for_owner(skale.wallet.address)

    assert isinstance(schains, list)
    assert set(schains[-1].keys()) == set(FIELDS)


def test_get_schains_for_node(skale):
    node_id = skale.nodes.node_name_to_index(DEFAULT_NODE_NAME)
    schains_for_node = skale.schains.get_schains_for_node(node_id)
    schain_ids_for_node = skale.schains_internal.get_schain_ids_for_node(node_id)

    assert isinstance(schains_for_node, list)
    assert len(schains_for_node) > 0
    assert len(schains_for_node) == len(schain_ids_for_node)

    test_schain = schains_for_node[0]
    schain_node_ids = skale.schains_internal.get_node_ids_for_schain(
        test_schain['name'])

    assert node_id in schain_node_ids


def test_name_to_id(skale):
    schain_id = skale.schains.name_to_id(DEFAULT_SCHAIN_NAME)
    assert schain_id == DEFAULT_SCHAIN_ID


def test_get_all_schains_ids(skale):
    schains_ids = skale.schains_internal.get_all_schains_ids()
    schain = skale.schains.get(schains_ids[-1])
    assert list(schain.keys()) == FIELDS


def test_get_schain_price(skale):
    for schain_type in SCHAIN_TYPES:
        schain_price = skale.schains.get_schain_price(SCHAIN_TYPES[schain_type],
                                                      LIFETIME_SECONDS)
        assert schain_price > 0
        assert type(schain_price) is int

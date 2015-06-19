from __future__ import unicode_literals, absolute_import

from itertools import combinations
from collections import OrderedDict
from datetime import datetime

from openvpn_status.models import Status, Client, Routing, GlobalStats


def is_inequality(iterable):
    return all(left != right for left, right in combinations(iterable, 2))


def test_status():
    status = Status()
    assert isinstance(status.client_list, OrderedDict)
    assert isinstance(status.routing_table, OrderedDict)

    assert hasattr(status, 'client_list')
    assert hasattr(status, 'routing_table')
    assert not hasattr(status, 'global_stats')
    assert not hasattr(status, 'updated_at')

    now = datetime.now()
    status.updated_at = now
    assert status.updated_at == now


def test_status_properties():
    status = Status()
    status.client_list.update((i, i) for i in range(3))
    assert len(status.client_list) == 3
    assert status.client_list[0] == 0
    assert status.client_list[1] == 1
    assert status.client_list[2] == 2


def test_status_labels():
    assert is_inequality([
        Status.client_list.label,
        Status.routing_table.label,
        Status.global_stats.label,
    ])


def test_client():
    client = Client()
    assert not hasattr(client, 'common_name')
    assert not hasattr(client, 'real_address')
    assert not hasattr(client, 'bytes_received')
    assert not hasattr(client, 'bytes_sent')
    assert not hasattr(client, 'connected_since')


def test_client_labels():
    assert is_inequality([
        Client.common_name.label,
        Client.real_address.label,
        Client.bytes_received.label,
        Client.bytes_sent.label,
        Client.connected_since.label,
    ])


def test_routing():
    routing = Routing()
    assert not hasattr(routing, 'virtual_address')
    assert not hasattr(routing, 'common_name')
    assert not hasattr(routing, 'real_address')
    assert not hasattr(routing, 'last_ref')


def test_routing_labels():
    assert is_inequality([
        Routing.virtual_address.label,
        Routing.common_name.label,
        Routing.real_address,
        Routing.last_ref,
    ])


def test_global_stats():
    global_stats = GlobalStats()
    assert not hasattr(global_stats, 'max_bcast_mcast_queue_len')

    global_stats.max_bcast_mcast_queue_len = 0
    assert global_stats.max_bcast_mcast_queue_len == 0

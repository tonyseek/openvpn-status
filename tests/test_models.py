from __future__ import absolute_import

from itertools import combinations
from collections import OrderedDict
from datetime import datetime
from ipaddress import IPv4Address

from openvpn_status.models import Status, Client, Routing, GlobalStats


def is_inequality(iterable):
    return all(left != right for left, right in combinations(iterable, 2))


def test_status():
    status = Status()
    assert isinstance(status.client_list, OrderedDict)
    assert isinstance(status.routing_table, OrderedDict)

    assert getattr(status, 'client_list', None) is not None
    assert getattr(status, 'routing_table', None) is not None
    assert getattr(status, 'global_stats', None) is None
    assert getattr(status, 'updated_at', None) is None

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
    assert getattr(client, 'common_name', None) is None
    assert getattr(client, 'real_address', None) is None
    assert getattr(client, 'bytes_received', None) is None
    assert getattr(client, 'bytes_sent', None) is None
    assert getattr(client, 'connected_since', None) is None

    client.bytes_received = 532895
    assert client.bytes_received.humanize() == u'532.9 kB'

    client.bytes_sent = 34254
    assert client.bytes_received.humanize(gnu=True) == u'520.4K'


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
    assert getattr(routing, 'virtual_address', None) is None
    assert getattr(routing, 'common_name', None) is None
    assert getattr(routing, 'real_address', None) is None
    assert getattr(routing, 'last_ref', None) is None

    routing.virtual_address = u'172.16.1.1'
    assert routing.virtual_address == IPv4Address(u'172.16.1.1')

    routing.real_address = u'192.168.1.1:8080'
    assert routing.real_address.host == IPv4Address(u'192.168.1.1')
    assert routing.real_address.port == 8080


def test_routing_labels():
    assert is_inequality([
        Routing.virtual_address.label,
        Routing.common_name.label,
        Routing.real_address,
        Routing.last_ref,
    ])


def test_global_stats():
    global_stats = GlobalStats()
    assert getattr(global_stats, 'max_bcast_mcast_queue_len', None) is None

    global_stats.max_bcast_mcast_queue_len = 0
    assert global_stats.max_bcast_mcast_queue_len == 0

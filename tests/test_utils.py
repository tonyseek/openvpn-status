from __future__ import unicode_literals, absolute_import

from datetime import datetime
from ipaddress import IPv4Address

from pytest import mark
from six import text_type

from openvpn_status.utils import (
    parse_time, parse_peer, parse_filesize, PeerAddress, FileSize)


@mark.parametrize('text,time', [
    ('Thu Jun 18 04:23:03 2015', datetime(2015, 6, 18, 4, 23, 3)),
    ('Thu Jun 18 04:08:39 2015', datetime(2015, 6, 18, 4, 8, 39)),
    ('Thu Jun 18 07:57:25 2015', datetime(2015, 6, 18, 7, 57, 25)),
    (datetime(2015, 6, 18, 7, 57, 25), datetime(2015, 6, 18, 7, 57, 25)),
])
def test_parse_time(text, time):
    assert parse_time(text) == time


@mark.parametrize('text,peer', [
    ('10.0.0.1:49502', PeerAddress(IPv4Address('10.0.0.1'), 49502)),
    ('10.0.0.2:64169', PeerAddress(IPv4Address('10.0.0.2'), 64169)),
    ('10.0.0.3:63414', PeerAddress(IPv4Address('10.0.0.3'), 63414)),
    (PeerAddress('10.0.0.1', 80), PeerAddress('10.0.0.1', 80)),
])
def test_parse_peer(text, peer):
    assert parse_peer(text) == peer
    assert text_type(text) == text_type(peer)


@mark.parametrize('text,humanized', [
    (10240, '10.2 kB'),
    ('10240', '10.2 kB'),
    (FileSize(10240), '10.2 kB'),
])
def test_parse_filesize(text, humanized):
    assert text_type(parse_filesize(text)) == humanized

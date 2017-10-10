from __future__ import absolute_import

from datetime import datetime
from ipaddress import IPv4Address

from pytest import mark
from six import text_type

from openvpn_status.utils import (
    parse_time, parse_peer, parse_filesize, PeerAddress, FileSize)


@mark.parametrize('text,time', [
    (u'Thu Jun 18 04:23:03 2015', datetime(2015, 6, 18, 4, 23, 3)),
    (u'Thu Jun 18 04:08:39 2015', datetime(2015, 6, 18, 4, 8, 39)),
    (u'Thu Jun 18 07:57:25 2015', datetime(2015, 6, 18, 7, 57, 25)),
    (datetime(2015, 6, 18, 7, 57, 25), datetime(2015, 6, 18, 7, 57, 25)),
])
def test_parse_time(text, time):
    assert parse_time(text) == time


@mark.parametrize('text,peer', [
    (u'10.0.0.1:49502', PeerAddress(IPv4Address(u'10.0.0.1'), 49502)),
    (u'10.0.0.2:64169', PeerAddress(IPv4Address(u'10.0.0.2'), 64169)),
    (u'10.0.0.3:63414', PeerAddress(IPv4Address(u'10.0.0.3'), 63414)),
    (PeerAddress(u'10.0.0.1', 80), PeerAddress(u'10.0.0.1', 80)),
])
def test_parse_peer(text, peer):
    assert parse_peer(text) == peer
    assert text_type(text) == text_type(peer)


@mark.parametrize('text,humanized', [
    (10240, u'10.2 kB'),
    (u'10240', u'10.2 kB'),
    (FileSize(10240), u'10.2 kB'),
])
def test_parse_filesize(text, humanized):
    assert text_type(parse_filesize(text)) == humanized

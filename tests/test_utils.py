from __future__ import absolute_import

from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network

from pytest import mark
from six import text_type
from netaddr import EUI, mac_unix

from openvpn_status.utils import (
    parse_time, parse_peer, parse_vaddr, parse_filesize,
    PeerAddress, FileSize)


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


@mark.parametrize('text,virtual_addr', [
    (u'10.0.0.1', IPv4Address(u'10.0.0.1')),
    (u'2001:db8:2de::e13', IPv6Address(u'2001:db8:2de::e13')),
    (u'10.200.0.0/16', IPv4Network(u'10.200.0.0/16')),
    (u'2001:db8::1000/124', IPv6Network(u'2001:db8::1000/124')),
    (u'28:d2:44:d4:e6:ea', EUI(u'28:d2:44:d4:e6:ea', dialect=mac_unix)),
])
def test_parse_vaddr(text, virtual_addr):
    assert parse_vaddr(text) == virtual_addr
    assert text_type(text) == text_type(virtual_addr)


@mark.parametrize('text,humanized', [
    (10240, u'10.2 kB'),
    (u'10240', u'10.2 kB'),
    (FileSize(10240), u'10.2 kB'),
])
def test_parse_filesize(text, humanized):
    assert text_type(parse_filesize(text)) == humanized

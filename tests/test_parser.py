from __future__ import absolute_import

import datetime
import ipaddress

from pytest import fixture, raises
from six import text_type
from netaddr import EUI

from openvpn_status.parser import LogParser, ParsingError


@fixture
def openvpn_status(datadir):
    return datadir.join('openvpn-status.txt')


@fixture
def broken_status(datadir):
    return datadir.join('broken-openvpn-status')


def test_parser(openvpn_status):
    parser = LogParser.fromstring(openvpn_status.read())
    status = parser.parse()

    assert len(status.client_list) == 5
    assert len(status.routing_table) == 9

    assert status.global_stats.max_bcast_mcast_queue_len == 0
    assert status.updated_at == datetime.datetime(2015, 6, 18, 8, 12, 15)

    client = status.client_list[u'10.10.10.10:49502']
    assert client.common_name == u'foo@example.com'
    assert text_type(client.real_address) == u'10.10.10.10:49502'
    assert text_type(client.real_address.host) == u'10.10.10.10'
    assert client.real_address.port == 49502
    assert client.connected_since == datetime.datetime(2015, 6, 18, 4, 23, 3)
    assert client.bytes_received == 334948
    assert client.bytes_sent == 1973012

    tun_routing = status.routing_table[u'192.168.255.134']
    assert isinstance(tun_routing.virtual_address, ipaddress.IPv4Address)
    assert text_type(tun_routing.virtual_address) == u'192.168.255.134'
    assert tun_routing.common_name == u'foo@example.com'
    assert text_type(tun_routing.real_address) == u'10.10.10.10:49502'
    assert tun_routing.last_ref == datetime.datetime(2015, 6, 18, 8, 12, 9)

    tap_routing = status.routing_table[u'22:1d:63:bf:62:38']
    assert isinstance(tap_routing.virtual_address, EUI)
    assert text_type(tap_routing.virtual_address) == u'22:1d:63:bf:62:38'
    assert tap_routing.common_name == u'tap@example.com'
    assert text_type(tap_routing.real_address) == u'10.0.0.100:55712'
    assert tap_routing.last_ref == datetime.datetime(2017, 10, 19, 20, 14, 19)

    ccd_routing = status.routing_table[u'10.200.0.0/16']
    assert isinstance(ccd_routing.virtual_address, ipaddress.IPv4Network)
    assert text_type(ccd_routing.virtual_address) == u'10.200.0.0/16'
    assert ccd_routing.common_name == u'baz@example.com'
    assert text_type(ccd_routing.real_address) == u'10.10.10.10:63414'
    assert ccd_routing.last_ref == datetime.datetime(2015, 6, 18, 8, 12, 9)

    ccd_v6_routing = status.routing_table[u'2001:db8::1000/124']
    assert isinstance(ccd_v6_routing.virtual_address, ipaddress.IPv6Network)
    assert text_type(ccd_v6_routing.virtual_address) == u'2001:db8::1000/124'
    assert ccd_v6_routing.common_name == u'baz@example.com'
    assert text_type(ccd_v6_routing.real_address) == u'10.10.10.10:63414'
    assert ccd_v6_routing.last_ref == datetime.datetime(2015, 6, 18, 8, 12, 9)


def test_parser_with_syntax_errors(broken_status):
    def catch_syntax_error(seq):
        datafile = broken_status.join('%d.txt' % seq)
        parser = LogParser.fromstring(datafile.read())
        with raises(ParsingError) as error:
            parser.parse()
        return error

    error = catch_syntax_error(0)
    assert not error.value.args[0].startswith('expected list')
    assert not error.value.args[0].startswith('expected 2-tuple')
    assert error.value.args[0].endswith('got end of input')

    error = catch_syntax_error(1)
    assert not error.value.args[0].startswith('expected list')
    assert not error.value.args[0].startswith('expected 2-tuple')
    assert error.value.args[0].endswith('got %r' % u'BrokenVPN CLIENT LIST')

    error = catch_syntax_error(2)
    assert error.value.args[0] == 'expected list but got end of input'

    error = catch_syntax_error(3)
    assert error.value.args[0] == 'expected 2-tuple but got end of input'

    error = catch_syntax_error(4)
    assert error.value.args[0] == \
        'expected 2-tuple but got %r' % u'Updated,Yo,Hoo'

    error = catch_syntax_error(5)
    assert error.value.args[0] == \
        'expected 2-tuple starting with %r' % u'Updated'

    error = catch_syntax_error(6)
    assert error.value.args[0] == 'expected list but got %r' % u'YO TABLE'

    error = catch_syntax_error(7)
    assert error.value.args[0].startswith('expected valid format: time data ')

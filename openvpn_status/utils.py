from __future__ import unicode_literals, absolute_import

import datetime
import collections
import ipaddress

from six import python_2_unicode_compatible as unicode_compatible


DATETIME_FORMAT_OPENVPN = '%a %b %d %H:%M:%S %Y'


def parse_time(time):
    """Parses date and time from input string in OpenVPN logging format."""
    if isinstance(time, datetime.datetime):
        return time
    return datetime.datetime.strptime(time, DATETIME_FORMAT_OPENVPN)


def parse_peer(peer):
    if isinstance(peer, PeerAddress):
        return peer
    host, port = peer.rsplit(':', 1)
    return PeerAddress(ipaddress.ip_address(host), int(port))


@unicode_compatible
class PeerAddress(collections.namedtuple('PeerAddress', 'host port')):
    """The address of peer entity."""

    def __str__(self):
        return '{0}:{1}'.format(self.host, self.port)

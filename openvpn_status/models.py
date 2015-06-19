from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from ipaddress import ip_address

from .descriptors import LabelProperty, name_descriptors
from .utils import parse_time, parse_peer, parse_filesize


@name_descriptors
class Status(object):
    """The OpenVPN status model."""

    client_list = LabelProperty('OpenVPN CLIENT LIST', OrderedDict)
    routing_table = LabelProperty('ROUTING TABLE', OrderedDict)
    global_stats = LabelProperty('GLOBAL STATS')
    updated_at = LabelProperty('Updated', input_type=parse_time)


@name_descriptors
class Client(object):
    """The OpenVPN client model."""

    common_name = LabelProperty('Common Name')
    real_address = LabelProperty('Real Address', input_type=parse_peer)
    bytes_received = LabelProperty('Bytes Received', input_type=parse_filesize)
    bytes_sent = LabelProperty('Bytes Sent', input_type=parse_filesize)
    connected_since = LabelProperty('Connected Since', input_type=parse_time)


@name_descriptors
class Routing(object):
    """The OpenVPN routing model."""

    virtual_address = LabelProperty('Virtual Address', input_type=ip_address)
    common_name = LabelProperty('Common Name')
    real_address = LabelProperty('Real Address', input_type=parse_peer)
    last_ref = LabelProperty('Last Ref', input_type=parse_time)


@name_descriptors
class GlobalStats(object):
    """The OpenVPN global stats model."""

    max_bcast_mcast_queue_len = LabelProperty(
        'Max bcast/mcast queue length', input_type=int)

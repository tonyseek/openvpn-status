from __future__ import absolute_import

from collections import OrderedDict

from .descriptors import LabelProperty, name_descriptors
from .utils import parse_time, parse_peer, parse_vaddr, parse_filesize


@name_descriptors
class Status(object):
    """The OpenVPN status model."""

    client_list = LabelProperty(u'OpenVPN CLIENT LIST', OrderedDict)
    routing_table = LabelProperty(u'ROUTING TABLE', OrderedDict)
    global_stats = LabelProperty(u'GLOBAL STATS')
    updated_at = LabelProperty(u'Updated', input_type=parse_time)


@name_descriptors
class Client(object):
    """The OpenVPN client model."""

    common_name = LabelProperty(u'Common Name')
    real_address = LabelProperty(u'Real Address', input_type=parse_peer)
    bytes_received = LabelProperty(
        u'Bytes Received', input_type=parse_filesize)
    bytes_sent = LabelProperty(u'Bytes Sent', input_type=parse_filesize)
    connected_since = LabelProperty(u'Connected Since', input_type=parse_time)


@name_descriptors
class Routing(object):
    """The OpenVPN routing model."""

    virtual_address = LabelProperty(u'Virtual Address', input_type=parse_vaddr)
    common_name = LabelProperty(u'Common Name')
    real_address = LabelProperty(u'Real Address', input_type=parse_peer)
    last_ref = LabelProperty(u'Last Ref', input_type=parse_time)


@name_descriptors
class GlobalStats(object):
    """The OpenVPN global stats model."""

    max_bcast_mcast_queue_len = LabelProperty(
        u'Max bcast/mcast queue length', input_type=int)

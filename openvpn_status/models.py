from __future__ import unicode_literals, absolute_import

from collections import OrderedDict

from .descriptors import LabelProperty, name_descriptors


@name_descriptors
class Status(object):
    """The OpenVPN status model."""

    client_list = LabelProperty('OpenVPN CLIENT LIST', OrderedDict)
    routing_table = LabelProperty('ROUTING TABLE', OrderedDict)
    global_stats = LabelProperty('GLOBAL STATS')
    updated_at = LabelProperty('Updated')


@name_descriptors
class Client(object):
    """The OpenVPN client model."""

    common_name = LabelProperty('Common Name')
    real_address = LabelProperty('Real Address')
    bytes_received = LabelProperty('Bytes Received')
    bytes_sent = LabelProperty('Bytes Sent')
    connected_since = LabelProperty('Connected Since')


@name_descriptors
class Routing(object):
    """The OpenVPN routing model."""

    virtual_address = LabelProperty('Virtual Address')
    common_name = LabelProperty('Common Name')
    real_address = LabelProperty('Real Address')
    last_ref = LabelProperty('Last Ref')


@name_descriptors
class GlobalStats(object):
    """The OpenVPN global stats model."""

    max_bcast_mcast_queue_len = LabelProperty('Max bcast/mcast queue length')

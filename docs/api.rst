API Reference
=============

Models
------

.. module:: openvpn_status.models

.. autoclass:: Status

   .. attribute:: client_list

      (:class:`~collections.OrderedDict`)

      The list of connected clients. The dictionary items have form of
      `(client.real_address, client)`. See also :class:`Client`.

   .. attribute:: routing_table

      :type: :class:`~collections.OrderedDict`

      The list of routing table. The dictionary items have form of
      `(routing.virtual_address, routing)`. See also :class:`Routing`.

   .. attribute:: global_stats

      :type: :class:`GlobalStats`

   .. attribute:: updated_at

      :type: :class:`datetime.datetime`

      The last updated time of log file in UTC.

.. autoclass:: Client

   .. attribute:: common_name

      :type: :class:`str`

      The common name of OpenVPN client certificate. (e.g. `foo@example.com`)

   .. attribute:: real_address

      :type: :class:`~.utils.PeerAddress`

      The real IP address and port of client.

   .. attribute:: bytes_received

      :type: :class:`~.utils.FileSize`

   .. attribute:: bytes_sent

      :type: :class:`~.utils.FileSize`

   .. attribute:: connected_since

      :type: :class:`datetime.datetime`

      The time in UTC since last connection established.

.. autoclass:: Routing

   .. attribute:: virtual_address

      :type:
          - :class:`ipaddress.IPv4Address` or :class:`ipaddress.IPv6Address`
            for TUN mode
          - :class:`netaddr.EUI` (MAC address) for TAP mode
          - :class:`ipaddress.IPv4Network` or :class:`ipaddress.IPv6Network`
            for *client-config-dir* and *iroute* enabled servers.

      Read more about TUN and TAP: `Bridging vs. routing`_.

      Read more about *client-config-dir* (CCD) and *iroute*: `Lans behind OpenVPN`_.

      .. _`Bridging vs. routing`: https://community.openvpn.net/openvpn/wiki/BridgingAndRouting
      .. _`Lans behind OpenVPN`: https://community.openvpn.net/openvpn/wiki/RoutedLans

   .. attribute:: common_name

      Same as :attr:`Client.common_name`

   .. attribute:: real_address

      Same as :attr:`Client.real_address`

   .. attribute:: last_ref

      :type: :class:`datetime.datetime`

.. autoclass:: GlobalStats

   .. attribute:: max_bcast_mcast_queue_len

      :type: :class:`int`


Parser
------

.. module:: openvpn_status.parser

.. autoclass:: LogParser
   :members:

.. autoexception:: ParsingError


Shortcuts
---------

.. module:: openvpn_status.shortcuts

.. autofunction:: parse_status

Utilties
--------

.. module:: openvpn_status.utils

.. autoclass:: PeerAddress
   :members:

.. autoclass:: FileSize
   :members:

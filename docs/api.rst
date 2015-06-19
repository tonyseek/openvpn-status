API Reference
=============

Models
------

.. module:: openvpn_status.models

.. autoclass:: Status

   .. attribute:: client_list

      (:class:`~collections.OrderedDict`)

      The list of connected clients. The dictionary items have form of
      `(client.common_name, client)`. See also :class:`Client`.

   .. attribute:: routing_table

      :type: :class:`~collections.OrderedDict`

      The list of routing table. The dictionary items have form of
      `(routing.common_name, routing)`. See also :class:`Routing`

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

      :type: :class:`~ipaddress.IPv4Address` or :class:`~ipaddress.IPv6Address`

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

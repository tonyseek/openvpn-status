|Build Status| |Coverage Status| |PyPI Version| |Wheel Status|

OpenVPN Status
==============

**openvpn-status** is a Python library. It parses OpenVPN status log and turns
it into Python data structure for you.

It is compatible with CPython `2.7`, `3.3`, `3.4` and PyPy.


Installation
------------

.. code-block:: bash

    pip install openvpn-status

Don't forget to put it in ``setup.py`` / ``requirements.txt``.


Getting Started
---------------

You could configure your OpenVPN server to log for client status. In usual it
could be achieved by adding ``status /path/to/openvpn-status.log`` line to
``/etc/openvpn/openvpn.conf``. For example::

    proto udp
    port 1194
    dev tun0
    status /var/run/openvpn-status.log

Once OpenVPN server running, the log file will be created and written. It looks
like::

    OpenVPN CLIENT LIST
    Updated,Thu Jun 18 08:12:15 2015
    Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since
    foo@example.com,10.10.10.10:49502,334948,1973012,Thu Jun 18 04:23:03 2015
    bar@example.com,10.10.10.10:64169,1817262,28981224,Thu Jun 18 04:08:39 2015
    ROUTING TABLE
    Virtual Address,Common Name,Real Address,Last Ref
    192.168.255.134,foo@example.com,10.10.10.10:49502,Thu Jun 18 08:12:09 2015
    192.168.255.126,bar@example.com,10.10.10.10:64169,Thu Jun 18 08:11:55 2015
    GLOBAL STATS
    Max bcast/mcast queue length,0
    END

Now we could parse log file with this library:

.. code-block:: python

    from openvpn_status import parse_status

    with open('/var/run/openvpn-status.log') as logfile:
        status = parse_status(logfile.read())

    print(status.updated_at)  # datetime.datetime(2015, 6, 18, 8, 12, 15)

    foo_client = status.client_list['foo@example.com']
    print(foo_client.bytes_received)  # 334.9 kB
    print(foo_client.bytes_sent)  # 2.0 MB


More detail and API reference are in the document_.


Contributing
------------

If you want to report bugs or request features, please feel free to open
issues on GitHub_.

Of course, pull requests are always welcome.


.. _document: https://openvpn-status.readthedocs.org
.. _GitHub: https://github.com/tonyseek/openvpn-status/issues

.. |Build Status| image:: https://img.shields.io/travis/tonyseek/openvpn-status.svg
   :target: https://travis-ci.org/tonyseek/openvpn-status
   :alt: Build Status
.. |Coverage Status| image:: https://img.shields.io/coveralls/tonyseek/openvpn-status.svg
   :target: https://coveralls.io/r/tonyseek/openvpn-status
   :alt: Coverage Status
.. |Wheel Status| image:: https://img.shields.io/pypi/wheel/openvpn-status.svg
   :target: https://warehouse.python.org/project/openvpn-status
   :alt: Wheel Status
.. |PyPI Version| image:: https://img.shields.io/pypi/v/openvpn-status.svg
   :target: https://pypi.python.org/pypi/openvpn-status
   :alt: PyPI Version

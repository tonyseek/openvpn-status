from __future__ import unicode_literals, absolute_import

import openvpn_status


def test_version():
    assert openvpn_status.__version__ == '0.1.0.dev0'

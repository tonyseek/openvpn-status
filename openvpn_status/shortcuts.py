from __future__ import unicode_literals, absolute_import

from .parser import LogParser


def parse_status(status_log, encoding='utf-8'):
    """Parses the status log of OpenVPN.

    :param status_log: The content of status log.
    :type status_log: :class:`str`
    :param encoding: Optional. The encoding of status log.
    :type encoding: :class:`str`
    :return: The instance of :class:`.models.Status`
    """
    if isinstance(status_log, bytes):
        status_log = status_log.decode(encoding)
    parser = LogParser.fromstring(status_log)
    return parser.parse()

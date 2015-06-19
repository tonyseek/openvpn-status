from __future__ import unicode_literals, absolute_import

from six import Iterator, next

from .models import Status, Client, Routing, GlobalStats
from .descriptors import iter_descriptors


class LogParser(Iterator):
    """The parser for parsing OpenVPN status log.

    This kind of parser is stateful. So the :meth:`LogParser.parse` could be
    called once in the same instance of parser.
    """

    list_separator = ','
    line_separator = '\n'
    terminator = 'END'

    def __init__(self, lines):
        self.lines = iter(lines)
        self._last_line = None
        self._rollback = False

    def __next__(self):
        if self._rollback:
            self._rollback = False
            return self._last_line
        while True:
            line = next(self.lines).strip()
            if line:
                self._last_line = line
                return line

    @classmethod
    def fromstring(cls, content):
        """Creates a parser from content of log.

        :param str content: The log content.
        :return: The parser instance.
        """
        return cls(content.strip().split(cls.line_separator))

    def rollback(self):
        self._rollback = True

    def expect_line(self, content):
        try:
            line = next(self)
        except StopIteration:
            raise ParsingError('expected %r but got end of input' % content)
        if line != content:
            raise ParsingError('expected %r but got %r' % (content, line))

    def expect_list(self):
        try:
            line = next(self)
        except StopIteration:
            raise ParsingError('expected list but got end of input')
        splited = line.split(self.list_separator)
        if len(splited) == 1:
            raise ParsingError('expected list but got %r' % line)
        return splited

    def expect_tuple(self, name):
        try:
            line = next(self)
        except StopIteration:
            raise ParsingError('expected 2-tuple but got end of input')
        splited = line.split(self.list_separator)
        if len(splited) != 2:
            raise ParsingError('expected 2-tuple but got %r' % line)
        if splited[0] != name:
            raise ParsingError('expected 2-tuple starting with %r' % name)
        return splited[1]

    def parse(self):
        """Parses the status log.

        :raises ParsingError: if syntax error found in the log.
        :return: The :class:`.models.Status` with filled data.
        """
        status = Status()
        self.expect_line(Status.client_list.label)

        status.updated_at = self.expect_tuple(Status.updated_at.label)
        status.client_list.update({
            c.common_name: c
            for c in self._parse_fields(Client, Status.routing_table.label)})
        status.routing_table.update({
            r.common_name: r
            for r in self._parse_fields(Routing, Status.global_stats.label)})
        status.global_stats = GlobalStats()
        status.global_stats.max_bcast_mcast_queue_len = self.expect_tuple(
            GlobalStats.max_bcast_mcast_queue_len.label)

        self.expect_line(self.terminator)
        return status

    def _parse_fields(self, cls, next_line):
        labels = self.expect_list()
        descriptors = iter_descriptors(cls)
        label_to_name = {
            descriptor.label: name for name, descriptor in descriptors}
        index_to_name = {
            index: label_to_name[label] for index, label in enumerate(labels)}

        while True:
            try:
                values = self.expect_list()
            except ParsingError as list_error:
                try:
                    self.rollback()
                    self.expect_line(next_line)
                except ParsingError as line_error:
                    raise ParsingError(*(list_error.args + line_error.args))
                else:
                    break

            instance = cls()
            for index, value in enumerate(values):
                name = index_to_name[index]
                setattr(instance, name, value)
            yield instance


class ParsingError(Exception):
    pass

from pytest import fixture, raises

from openvpn_status.parser import LogParser, ParsingError


@fixture
def openvpn_status(datadir):
    return datadir.join('openvpn-status.txt')


@fixture
def broken_status(datadir):
    return datadir.join('broken-openvpn-status')


def test_parser(openvpn_status):
    parser = LogParser.fromstring(openvpn_status.read())
    status = parser.parse()

    assert len(status.client_list) == 3
    assert len(status.routing_table) == 3
    assert status.global_stats
    assert status.updated_at


def test_parser_with_syntax_errors(broken_status):
    def catch_syntax_error(seq):
        datafile = broken_status.join('%d.txt' % seq)
        parser = LogParser.fromstring(datafile.read())
        with raises(ParsingError) as error:
            parser.parse()
        return error

    error = catch_syntax_error(0)
    assert not error.value.args[0].startswith('expected list')
    assert not error.value.args[0].startswith('expected 2-tuple')
    assert error.value.args[0].endswith('got end of input')

    error = catch_syntax_error(1)
    assert not error.value.args[0].startswith('expected list')
    assert not error.value.args[0].startswith('expected 2-tuple')
    assert error.value.args[0].endswith('got %r' % u'BrokenVPN CLIENT LIST')

    error = catch_syntax_error(2)
    assert error.value.args[0] == 'expected list but got end of input'

    error = catch_syntax_error(3)
    assert error.value.args[0] == 'expected 2-tuple but got end of input'

    error = catch_syntax_error(4)
    assert error.value.args[0] == \
        'expected 2-tuple but got %r' % u'Updated,Yo,Hoo'

    error = catch_syntax_error(5)
    assert error.value.args[0] == \
        'expected 2-tuple starting with %r' % u'Updated'

    error = catch_syntax_error(6)
    assert error.value.args[0] == 'expected list but got %r' % u'YO TABLE'

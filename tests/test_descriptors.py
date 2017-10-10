from __future__ import absolute_import

from pytest import fixture, raises

from openvpn_status.descriptors import (
    LabelProperty, name_descriptors, iter_descriptors)


@fixture
def foo_class():
    @name_descriptors
    class Foo(object):
        foo = LabelProperty('Foo')
        bar = LabelProperty('Bar', default=lambda: 0, input_type=int)
        baz = property(lambda self: self.bar)
        biu = ()
    return Foo


def test_label_and_its_name(foo_class):
    foo = foo_class()
    with raises(AttributeError):
        foo.foo
    assert foo.bar is 0
    assert foo.baz is 0

    foo.foo = u'1'
    foo.bar = u'2'

    assert foo.foo == u'1'
    assert foo.bar == 2
    assert foo.baz == 2


def test_iter_descriptors(foo_class):
    assert dict(iter_descriptors(foo_class)) == {
        'foo': foo_class.foo,
        'bar': foo_class.bar,
        'baz': foo_class.baz,
    }

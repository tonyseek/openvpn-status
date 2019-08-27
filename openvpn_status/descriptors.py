from __future__ import absolute_import

from six import iteritems


class LabelProperty(object):
    """The property with label name."""

    def __init__(self, label, default=None, input_type=None):
        self.label = label
        self.default = default
        self.input_type = input_type
        self.__name__ = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.__name__ in instance.__dict__:
            return instance.__dict__[self.__name__]
        elif self.default is not None:
            value = self.default()
            instance.__dict__[self.__name__] = value
            return value
        else:
            names = (owner.__name__, self.__name__)
            raise AttributeError('%r object has no attribute %r' % names)

    def __set__(self, instance, value):
        if self.input_type is not None:
            try:
                value = self.input_type(value)
            except ValueError as e:
                raise AssignmentValueError(e)
        instance.__dict__[self.__name__] = value


_missing = object()


def name_descriptors(cls):
    for name, value in iter_descriptors(cls):
        if getattr(value, '__name__', _missing) is None:
            value.__name__ = name
    return cls


def iter_descriptors(cls):
    for name, value in iteritems(cls.__dict__):
        if name.startswith('__'):
            continue
        if getattr(value, '__get__', None) or getattr(value, '__set__', None):
            yield name, value


class AssignmentValueError(ValueError):
    pass

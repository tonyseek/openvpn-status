from __future__ import unicode_literals, absolute_import


class LabelProperty(object):
    """The property with label name."""

    def __init__(self, label, default_factory=None):
        self.label = label
        self.default_factory = default_factory

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.__name__ in instance.__dict__:
            return instance.__dict__[self.__name__]
        elif self.default_factory is not None:
            return self.default_factory()
        else:
            names = (owner.__name__, self.__name__)
            raise AttributeError('%r object has no attribute %r' % names)

    def __set__(self, instance, value):
        instance.__dict__[self.__name__] = value


def name_descriptors(cls):
    for name, value in iter_descriptors(cls):
        if not hasattr(value, '__name__'):
            value.__name__ = name
    return cls


def iter_descriptors(cls):
    for name, value in cls.__dict__.items():
        if name.startswith('__'):
            continue
        if hasattr(value, '__get__') or hasattr(value, '__set__'):
            yield name, value

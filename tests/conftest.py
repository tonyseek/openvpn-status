from __future__ import absolute_import

from pytest import fixture
from py.path import local


@fixture
def datadir():
    return local(__file__).dirpath('data')

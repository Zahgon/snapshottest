import math
from collections import defaultdict
from enum import Enum

from .sorted_dict import SortedDict
from .generic_repr import GenericRepr


class BaseFormatter(object):
    def can_format(self, value):
        raise NotImplementedError()

    def format(self, value, indent, formatter):
        raise NotImplementedError()

    def get_imports(self):
        pass

    def assert_value_matches_snapshot(
        self, test, test_value, snapshot_value, formatter
    ):
        test.assert_equals(formatter.normalize(test_value), snapshot_value)

    def store(self, test, value):
        return value

    def normalize(self, value, formatter):
        return value


class TypeFormatter(BaseFormatter):
    def __init__(self, types, format_func):
        self.types = types
        self.format_func = format_func

    def can_format(self, value):
        return isinstance(value, self.types)

    def format(self, value, indent, formatter):
        pass


class CollectionFormatter(TypeFormatter):
    def normalize(self, value, formatter):
        iterator = iter(value.items()) if isinstance(value, dict) else iter(value)
        # https://github.com/syrusakbary/snapshottest/issues/115
        # Normally we shouldn't need to turn this into a list, but some iterable
        # constructors need a list not an iterator (e.g. unittest.mock.call).
        return value.__class__([formatter.normalize(item) for item in iterator])


class DefaultDictFormatter(TypeFormatter):
    def normalize(self, value, formatter):
        return defaultdict(
            value.default_factory, (formatter.normalize(item) for item in value.items())
        )


def trepr(s):
    pass


def format_none(value, indent, formatter):
    pass


def format_str(value, indent, formatter):
    pass


def format_float(value, indent, formatter):
    pass


def format_std_type(value, indent, formatter):
    pass


def format_dict(value, indent, formatter):
    pass


def format_list(value, indent, formatter):
    pass


def format_sequence(value, indent, formatter):
    pass


def format_tuple(value, indent, formatter):
    pass


def format_set(value, indent, formatter):
    pass


def format_frozenset(value, indent, formatter):
    pass


def format_enum(value, indent, formatter):
    pass


class GenericFormatter(BaseFormatter):
    def can_format(self, value):
        return True

    def store(self, test, value):
        return GenericRepr.from_value(value)

    def normalize(self, value, formatter):
        return GenericRepr.from_value(value)

    def format(self, value, indent, formatter):
        pass

    def get_imports(self):
        pass

    def assert_value_matches_snapshot(
        self, test, test_value, snapshot_value, formatter
    ):
        test_value = GenericRepr.from_value(test_value)
        # Assert equality between the representations to provide a nice textual diff.
        test.assert_equals(test_value.representation, snapshot_value.representation)


def default_formatters():
    return [
        TypeFormatter(type(None), format_none),
        TypeFormatter((Enum,), format_enum),
        DefaultDictFormatter(defaultdict, format_dict),
        CollectionFormatter(dict, format_dict),
        CollectionFormatter(tuple, format_tuple),
        CollectionFormatter(list, format_list),
        CollectionFormatter(set, format_set),
        CollectionFormatter(frozenset, format_frozenset),
        TypeFormatter((str,), format_str),
        TypeFormatter((float,), format_float),
        TypeFormatter((int, complex, bool, bytes), format_std_type),
        GenericFormatter(),
    ]

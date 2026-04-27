import codecs
import errno
import os
import sys
import importlib.util
from collections import defaultdict
import logging

from .snapshot import Snapshot
from .formatter import Formatter
from .error import SnapshotNotFound


logger = logging.getLogger(__name__)


def _escape_quotes(text):
    pass


def _load_source(module_name, filepath):
    """
    Replaces old imp.load_source() call.
    
    The imp module was dropped in Python 3.12 in favor of the importlib.
    See: https://docs.python.org/3.11/library/imp.html#imp.load_module
    
    Following code was inspired by the importlib documentation example: 
    https://docs.python.org/3.12/library/importlib.html#importing-a-source-file-directly
    
    This approach has been also encouraged in the official mailing lists:
    https://discuss.python.org/t/how-do-i-migrate-from-imp/27885 
    """
    pass


class SnapshotModule(object):
    _snapshot_modules = {}
    _before_write_callbacks = []

    def __init__(self, module, filepath):
        self._original_snapshot = None
        self._snapshots = None
        self.module = module
        self.filepath = filepath
        self.imports = defaultdict(set)
        self.visited_snapshots = set()
        self.new_snapshots = set()
        self.failed_snapshots = set()
        self.imports["snapshottest"].add("Snapshot")

    def load_snapshots(self):
        pass

    def visit(self, snapshot_name):
        self.visited_snapshots.add(snapshot_name)

    def delete_unvisited(self):
        pass

    @property
    def unvisited_snapshots(self):
        pass

    @classmethod
    def total_unvisited_snapshots(cls):
        pass

    @classmethod
    def get_modules(cls):
        pass

    @classmethod
    def stats_for_module(cls, getter):
        count_snapshots = 0
        count_modules = 0
        for module in SnapshotModule._snapshot_modules.values():
            length = getter(module)
            count_snapshots += length
            count_modules += min(length, 1)

        return count_snapshots, count_modules

    @classmethod
    def stats_unvisited_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.unvisited_snapshots))

    @classmethod
    def stats_visited_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.visited_snapshots))

    @classmethod
    def stats_new_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.new_snapshots))

    @classmethod
    def stats_failed_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.failed_snapshots))

    @classmethod
    def stats_successful_snapshots(cls):
        stats_visited = cls.stats_visited_snapshots()
        stats_failed = cls.stats_failed_snapshots()
        return stats_visited[0] - stats_failed[0]

    @classmethod
    def has_snapshots(cls):
        pass

    @property
    def original_snapshot(self):
        pass

    @property
    def snapshots(self):
        pass

    def __getitem__(self, test_name):
        try:
            return self.snapshots[test_name]
        except KeyError:
            raise SnapshotNotFound(self, test_name)

    def __setitem__(self, key, value):
        if key not in self.snapshots:
            # It's a new test
            self.new_snapshots.add(key)
        self.snapshots[key] = value

    def mark_failed(self, key):
        return self.failed_snapshots.add(key)

    @property
    def snapshot_dir(self):
        pass

    def save(self):
        pass

    def _apply_callbacks(self, data):
        pass

    @classmethod
    def get_module_for_testpath(cls, test_filepath):
        pass

    @classmethod
    def register_before_file_write_callback(cls, callback):
        pass

    @classmethod
    def clear_before_file_write_callbacks(cls):
        pass


class SnapshotTest(object):
    _current_tester = None

    def __init__(self):
        self.curr_snapshot = ""
        self.snapshot_counter = 1

    @property
    def module(self):
        raise NotImplementedError("module property needs to be implemented")

    @property
    def update(self):
        pass

    @property
    def test_name(self):
        raise NotImplementedError("test_name property needs to be implemented")

    def __enter__(self):
        SnapshotTest._current_tester = self
        return self

    def __exit__(self, type, value, tb):
        self.save_changes()
        SnapshotTest._current_tester = None

    def visit(self):
        self.module.visit(self.test_name)

    def fail(self):
        self.module.mark_failed(self.test_name)

    def store(self, data):
        formatter = Formatter.get_formatter(data)
        data = formatter.store(self, data)
        self.module[self.test_name] = data

    def assert_value_matches_snapshot(self, test_value, snapshot_value):
        formatter = Formatter.get_formatter(test_value)
        formatter.assert_value_matches_snapshot(
            self, test_value, snapshot_value, Formatter()
        )

    def assert_equals(self, value, snapshot):
        assert value == snapshot

    def assert_match(self, value, name=""):
        self.curr_snapshot = name or self.snapshot_counter
        self.visit()
        if self.update:
            self.store(value)
        else:
            try:
                prev_snapshot = self.module[self.test_name]
            except SnapshotNotFound:
                self.store(value)  # first time this test has been seen
            else:
                try:
                    self.assert_value_matches_snapshot(value, prev_snapshot)
                except AssertionError:
                    self.fail()
                    raise

        if not name:
            self.snapshot_counter += 1

    def save_changes(self):
        pass


def assert_match_snapshot(value, name=""):
    if not SnapshotTest._current_tester:
        raise Exception(
            "You need to use assert_match_snapshot in the SnapshotTest context."
        )

    SnapshotTest._current_tester.assert_match(value, name)

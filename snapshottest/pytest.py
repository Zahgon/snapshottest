import pytest
import re

from .module import SnapshotModule, SnapshotTest
from .diff import PrettyDiff
from .reporting import reporting_lines, diff_report


def pytest_addoption(parser):
    pass


class PyTestSnapshotTest(SnapshotTest):
    def __init__(self, request=None):
        self.request = request
        super(PyTestSnapshotTest, self).__init__()

    @property
    def module(self):
        pass

    @property
    def update(self):
        pass

    @property
    def test_name(self):
        pass


class SnapshotSession(object):
    def __init__(self, config):
        self.verbose = config.getoption("snapshot_verbose")
        self.config = config

    def display(self, tr):
        pass


def pytest_assertrepr_compare(op, left, right):
    pass


@pytest.fixture
def snapshot(request):
    pass


def pytest_terminal_summary(terminalreporter):
    pass


# force the other plugins to initialise first
# (fixes issue with capture not being properly initialised)
@pytest.mark.trylast
def pytest_configure(config):
    pass
    # config.pluginmanager.register(bs, "snapshottest")

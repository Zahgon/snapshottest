import logging
import os

from nose.plugins import Plugin

from .module import SnapshotModule
from .reporting import reporting_lines
from .unittest import TestCase

log = logging.getLogger("nose.plugins.snapshottest")


class SnapshotTestPlugin(Plugin):
    name = "snapshottest"
    enabled = True

    separator1 = "=" * 70
    separator2 = "-" * 70

    def options(self, parser, env=os.environ):
        pass

    def configure(self, options, conf):
        pass

    def wantClass(self, cls):
        pass

    def afterContext(self):
        pass

    def report(self, stream):
        pass

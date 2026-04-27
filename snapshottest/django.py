from django.test import TestCase as dTestCase
from django.test import SimpleTestCase as dSimpleTestCase
from django.test.runner import DiscoverRunner

from snapshottest.reporting import reporting_lines
from .unittest import TestCase as uTestCase
from .module import SnapshotModule


class TestRunnerMixin(object):
    separator1 = "=" * 70
    separator2 = "-" * 70

    def __init__(self, snapshot_update=False, **kwargs):
        super(TestRunnerMixin, self).__init__(**kwargs)
        uTestCase.snapshot_should_update = snapshot_update

    @classmethod
    def add_arguments(cls, parser):
        pass

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        pass

    def print_report(self):
        pass


class TestRunner(TestRunnerMixin, DiscoverRunner):
    pass


class TestCase(uTestCase, dTestCase):
    pass


class SimpleTestCase(uTestCase, dSimpleTestCase):
    pass

import unittest
import inspect

from .module import SnapshotModule, SnapshotTest
from .diff import PrettyDiff
from .reporting import diff_report


class UnitTestSnapshotTest(SnapshotTest):
    def __init__(self, test_class, test_id, test_filepath, should_update, assertEqual):
        self.test_class = test_class
        self.test_id = test_id
        self.test_filepath = test_filepath
        self.assertEqual = assertEqual
        self.should_update = should_update
        super(UnitTestSnapshotTest, self).__init__()

    @property
    def module(self):
        pass

    @property
    def update(self):
        pass

    def assert_equals(self, value, snapshot):
        self.assertEqual(value, snapshot)

    @property
    def test_name(self):
        pass


# Inspired by https://gist.github.com/twolfson/13f5f5784f67fd49b245
class TestCase(unittest.TestCase):

    snapshot_should_update = False

    @classmethod
    def setUpClass(cls):
        """On inherited classes, run our `setUp` method"""
        pass

    def comparePrettyDifs(self, obj1, obj2, msg):
        # self
        # assert obj1 == obj2
        pass
        #     raise self.failureException("DIFF")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """Do some custom setup"""
        pass

    def tearDown(self):
        """Do some custom setup"""
        pass

    def assert_match_snapshot(self, value, name=""):
        self._snapshot.assert_match(value, name=name)

    assertMatchSnapshot = assert_match_snapshot

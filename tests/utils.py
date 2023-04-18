import pytest


class FixturesTestCaseMixin(object):
    """
    Mixin to inject pytest fixtures on testcase.

    These fixtures will be available for every tests from the TestCase class.
    """

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tests_settings):
        self._caplog = caplog
        self._tests_settings = tests_settings

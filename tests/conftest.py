"""
Some fixture methods
"""
import os
import pytest

import cmsplugin_blocks


class FixturesSettingsTestMixin(object):
    """Mixin containing some basic settings for tests"""
    def __init__(self):
        # Base fixture datas directory
        self.tests_dir = 'tests'
        self.tests_path = os.path.normpath(
            os.path.join(
                os.path.abspath(os.path.dirname(cmsplugin_blocks.__file__)),
                '..',
                self.tests_dir,
            )
        )
        self.fixtures_dir = 'data_fixtures'
        self.fixtures_path = os.path.join(
            self.tests_path,
            self.fixtures_dir
        )


@pytest.fixture(scope="module")
def testsettings():
    """Initialize and return settings (mostly paths) for fixtures (scope at module level)"""
    return FixturesSettingsTestMixin()

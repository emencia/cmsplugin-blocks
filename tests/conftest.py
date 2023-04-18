"""
Some fixture methods
"""
from pathlib import Path

import pytest

import cmsplugin_blocks


class FixturesSettingsTestMixin(object):
    """
    A mixin containing settings about project. This is almost about useful
    paths which may be used in tests.

    Attributes:
        application_path (str): Absolute path to the application directory.
        package_path (str): Absolute path to the package directory.
        project_dir (pathlib.Path): Django project directory name.
        project_path (pathlib.Path): Absolute path to the Django project directory.
        tests_dir (pathlib.Path): Directory name which include tests.
        tests_path (pathlib.Path): Absolute path to the tests directory.
        fixtures_dir (pathlib.Path): Directory name which include tests datas.
        fixtures_path (pathlib.Path): Absolute path to the tests datas.
    """
    def __init__(self):
        self.application_path = Path(cmsplugin_blocks.__file__).parents[0].resolve()

        self.package_path = self.application_path.parent

        self.project_dir = "sandbox"
        self.project_path = self.package_path / self.project_dir

        self.tests_dir = "tests"
        self.tests_path = self.package_path / self.tests_dir

        self.fixtures_dir = "data_fixtures"
        self.fixtures_path = self.tests_path / self.fixtures_dir

    def format(self, content):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        return content.format(
            HOMEDIR=Path.home(),
            PACKAGE=str(self.package_path),
            APPLICATION=str(self.application_path),
            PROJECT=str(self.project_path),
            TESTS=str(self.tests_path),
            FIXTURES=str(self.fixtures_path),
            VERSION=cmsplugin_blocks.__version__,
        )


@pytest.fixture(scope="module")
def tests_settings():
    """
    Initialize and return settings for tests.

    Example:
        You may use it in tests like this: ::

            def test_foo(tests_settings):
                print(tests_settings.package_path)
                print(tests_settings.format("foo: {VERSION}"))
    """
    return FixturesSettingsTestMixin()


@pytest.fixture(scope="function")
def temp_builds_dir(tmp_path):
    """
    Prepare a temporary build directory.

    NOTE: You should use directly the "tmp_path" fixture in your tests.
    """
    return tmp_path

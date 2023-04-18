import pytest

from django.core.exceptions import ValidationError

from cmsplugin_blocks.utils import validate_css_classname, validate_css_classnames


@pytest.mark.parametrize("name", [
    "foo",
    "foo-bar",
    "foo_bar",
    "foo42bar",
    "_foo",
    "-foo",
])
def test_validate_css_classname_success(name):
    """
    A valid CSS class name should be correctly validated.
    """
    assert validate_css_classname(name) is True


@pytest.mark.parametrize("name", [
    "1foo",
    "foo bar",
    ".foo",
    "foo@bar",
])
def test_validate_css_classname_fail(name):
    """
    An invalid CSS class name should trigger a 'ValidationError' exception.
    """
    with pytest.raises(ValidationError):
        validate_css_classname(name)


def test_validate_css_classnames_success():
    """
    Every valid CSS class name should be correctly validated.
    """
    assert validate_css_classnames([
        "foo",
        "foo-bar",
        "foo_bar",
        "foo42bar",
        "_foo",
        "-foo",
    ]) is True


def test_validate_css_classnames_fail():
    """
    Any invalid CSS class name should trigger a 'ValidationError' exception.
    """
    with pytest.raises(ValidationError):
        validate_css_classnames([
            "foo",
            "1foo",
            "foo-bar",
        ])

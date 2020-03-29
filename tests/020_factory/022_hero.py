import pytest

from cmsplugin_blocks.choices_helpers import get_hero_default_template
from cmsplugin_blocks.factories.hero import HeroFactory


def test_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = HeroFactory()
    assert instance.template == get_hero_default_template()

    instance = HeroFactory(template="foo")
    assert instance.template == "foo"

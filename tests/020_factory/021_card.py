import pytest

from cmsplugin_blocks.choices_helpers import get_card_default_template
from cmsplugin_blocks.cms_plugins import CardPlugin
from cmsplugin_blocks.factories.card import CardFactory


def test_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = CardFactory()
    assert instance.template == get_card_default_template()

    instance = CardFactory(template="foo")
    assert instance.template == "foo"

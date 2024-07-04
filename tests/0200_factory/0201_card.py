from cmsplugin_blocks.choices_helpers import get_card_template_default
from cmsplugin_blocks.factories import CardFactory


def test_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = CardFactory()
    assert instance.template == get_card_template_default()

    instance = CardFactory(template="foo")
    assert instance.template == "foo"

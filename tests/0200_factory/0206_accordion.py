from cmsplugin_blocks.choices_helpers import get_accordion_template_default
from cmsplugin_blocks.factories import AccordionFactory, AccordionItemFactory


def test_accordion_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = AccordionFactory()
    assert instance.template == get_accordion_template_default()

    instance = AccordionFactory(template="foo")
    assert instance.template == "foo"


def test_item_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    accordion = AccordionFactory()

    instance = AccordionItemFactory(accordion=accordion, title="foo")
    assert instance.title == "foo"
    assert instance.accordion == accordion

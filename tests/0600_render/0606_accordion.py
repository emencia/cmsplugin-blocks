import logging

from cmsplugin_blocks.cms_plugins import AccordionPlugin
from cmsplugin_blocks.factories import (
    AccordionFactory, AccordionItemFactory, FeatureFactory
)
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase
from cmsplugin_blocks.utils.tests import html_pyquery

from tests.utils import FixturesTestCaseMixin


class AccordionRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Accordion plugin render tests case
    """

    def test_empty(self):
        """
        When there is no item, there should not be any HTML item part
        """
        accordion = AccordionFactory(title="Lorem ipsum dolore")

        placeholder, model_instance, context, html = self.create_basic_render(
            AccordionPlugin,
            template=accordion.template,
            title=accordion.title,
        )

        # Parse resulting plugin HTML render
        dom = html_pyquery(html)

        # Check title
        accordion_title = dom.find(".accordion__title")
        assert len(accordion_title) == 1
        assert accordion_title[0].text.strip() == accordion.title

        accordion_items = dom.find(".accordion__item")
        assert len(accordion_items) == 0

    def test_single_full_item(self):
        """
        Full single item should build all HTML parts
        """
        accordion = AccordionFactory.create()
        item = AccordionItemFactory.create(accordion=accordion)

        placeholder, model_instance, context, html = self.create_basic_render(
            AccordionPlugin,
            copy_relations_from=accordion,
            template=accordion.template,
            title=accordion.title,
        )

        dom = html_pyquery(html)

        # Check title
        accordion_title = dom.find(".accordion__title")
        assert len(accordion_title) == 1
        assert accordion_title[0].text.strip() == accordion.title

        # Item image and title
        accordion_item = dom.find(".accordion__item")[0]
        expected = "background-image: url(/media/cache/"
        assert accordion_item.get("style").startswith(expected) is True

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        item_title = accordion_item.cssselect(".accordion__item-title")[0]
        assert item_title.text.strip() == item.title

        # Item content
        item_content = accordion_item.cssselect(".accordion__item-content")[0]
        assert item_content.text.strip() == item.content

    def test_no_item_content(self):
        """
        When item content is empty, its HTML part should not be present
        """
        accordion = AccordionFactory()
        AccordionItemFactory.create(
            accordion=accordion,
            content="",
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AccordionPlugin,
            copy_relations_from=accordion,
            template=accordion.template,
            title=accordion.title,
        )

        dom = html_pyquery(html)

        item_content = dom.find(".accordion__item-content")
        assert len(item_content) == 0

    def test_many_item(self):
        """
        When accordion has many item, every item titles should be here
        """
        accordion = AccordionFactory()

        item_first = AccordionItemFactory.create(
            accordion=accordion,
        )
        item_second = AccordionItemFactory.create(
            accordion=accordion,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AccordionPlugin,
            copy_relations_from=accordion,
            template=accordion.template,
            title=accordion.title,
        )

        dom = html_pyquery(html)

        # Item titles
        item_titles = dom.find(".accordion__item-title")
        assert len(item_titles) == 2
        assert item_titles[0].text.strip() == item_first.title
        assert item_titles[1].text.strip() == item_second.title

    def test_feature_classes(self):
        """
        When accordion has features, their classes should be in .accordion 'class'
        attribute without duplicates.
        """
        feature_foo = FeatureFactory(
            value="foo",
            scope="size",
            plugins=["Container", "Accordion"],
        )
        feature_bar = FeatureFactory(
            value="bar",
            scope="color",
            plugins=["Accordion"]
        )
        feature_foobis = FeatureFactory(
            value="foo",
            scope="extra",
            plugins=["Container", "Accordion"],
        )

        accordion = AccordionFactory(
            fill_size_features=[feature_foo],
            fill_color_features=[feature_bar],
            fill_extra_features=[feature_foobis],
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AccordionPlugin,
            template=accordion.template,
            title=accordion.title,
            copy_relations_from=accordion,
        )

        dom = html_pyquery(html)
        features_classnames = [
            item
            for item in dom.attr("class").split()
            if item != "accordion"
        ]
        assert features_classnames == [
            "bar",
            "foo",
        ]

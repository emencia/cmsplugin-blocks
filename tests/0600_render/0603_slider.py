import logging

from cmsplugin_blocks.cms_plugins import SliderPlugin
from cmsplugin_blocks.factories import SliderFactory, SlideItemFactory
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase
from cmsplugin_blocks.utils.tests import html_pyquery

from tests.utils import FixturesTestCaseMixin


class SliderRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Slider plugin render tests case
    """

    def test_empty(self):
        """
        When there is no item, there should not be any HTML item part
        """
        slider = SliderFactory(title="Lorem ipsum dolore")

        placeholder, model_instance, context, html = self.create_basic_render(
            SliderPlugin,
            template=slider.template,
            title=slider.title,
        )

        # Parse resulting plugin HTML render
        dom = html_pyquery(html)

        # Check title
        slider_title = dom.find(".slider__title")
        assert len(slider_title) == 1
        assert slider_title[0].text.strip() == slider.title

        slider_items = dom.find(".slider__item")
        assert len(slider_items) == 0

    def test_single_full_item(self):
        """
        Full single item should build all HTML parts
        """
        slider = SliderFactory.create()
        item = SlideItemFactory.create(
            slider=slider,
            link_name="CTA link",
            link_url="http://perdu.com",
            link_open_blank=True,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            SliderPlugin,
            copy_relations_from=slider,
            template=slider.template,
            title=slider.title,
        )

        dom = html_pyquery(html)

        # Check title
        slider_title = dom.find(".slider__title")
        assert len(slider_title) == 1
        assert slider_title[0].text.strip() == slider.title

        # Item image and title
        slider_item = dom.find(".slider__item")[0]
        expected = "background-image: url(/media/cache/"
        assert slider_item.get("style").startswith(expected) is True

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        item_title = slider_item.cssselect(".slider__item-title")[0]
        assert item_title.text.strip() == item.title

        # Item content
        item_content = slider_item.cssselect(".slider__item-content")[0]
        assert item_content.text.strip() == item.content

        # Item link
        item_link = slider_item.cssselect(".slider__item-link a")[0]
        assert item_link.get("href") == item.link_url
        assert item_link.get("target") == "_blank"
        assert item_link.text.strip() == item.link_name

    def test_no_item_content(self):
        """
        When item content is empty, its HTML part should not be present
        """
        slider = SliderFactory()
        SlideItemFactory.create(
            slider=slider,
            content="",
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            SliderPlugin,
            copy_relations_from=slider,
            template=slider.template,
            title=slider.title,
        )

        dom = html_pyquery(html)

        item_content = dom.find(".slider__item-content")
        assert len(item_content) == 0

    def test_many_item(self):
        """
        When slider has many item, every item titles should be here
        """
        slider = SliderFactory()

        item_first = SlideItemFactory.create(
            slider=slider,
        )
        item_second = SlideItemFactory.create(
            slider=slider,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            SliderPlugin,
            copy_relations_from=slider,
            template=slider.template,
            title=slider.title,
        )

        dom = html_pyquery(html)

        # Item titles
        item_titles = dom.find(".slider__item-title")
        assert len(item_titles) == 2
        assert item_titles[0].text.strip() == item_first.title
        assert item_titles[1].text.strip() == item_second.title

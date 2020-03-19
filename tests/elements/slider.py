import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cms.api import add_plugin
from cms.models import Placeholder

from cmsplugin_blocks.choices_helpers import get_slider_default_template
from cmsplugin_blocks.models import Slider
from cmsplugin_blocks.cms_plugins import SliderPlugin
from cmsplugin_blocks.factories.slider import SliderFactory, SlideItemFactory


def test_factory(db):
    """
    Factory should correctly create a new plugin object without any errors
    """
    instance = SliderFactory()
    assert instance.template == get_slider_default_template()

    instance = SliderFactory(template="foo")
    assert instance.template == "foo"


def test_model_str(db, settings):
    """
    Model str should be correct in any case and truncated to 4 words with
    stripped HTML.
    """
    # Default filling from factory
    instance = SliderFactory()
    assert len(str(instance)) > 0

    # Empty content
    instance = SliderFactory(title="")
    assert len(str(instance)) == 0

    # Content with HTML and unicode
    instance = SliderFactory(
        title=(
            """Lorem ipsum"""
        )
    )
    assert str(instance) == "Lorem ipsum"


class SliderCMSPluginsTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Slider plugin tests case"""

    def test_plugin_render_empty(self):
        """
        When there is no item, there should not be any HTML item part
        """
        # Create random values for parameters with a factory
        slider = SliderFactory(title="Lorem ipsum dolore")

        placeholder, model_instance, context, html = self.create_basic_render(
            SliderPlugin,
            template=slider.template,
            title=slider.title,
        )

        expected_title = """<p class="slider__title">{}</p>""".format(
            slider.title
        )
        self.assertInHTML(expected_title, html)

        expected_empty_items = """<div class="slider__items"></div>"""
        self.assertInHTML(expected_empty_items, html)

    def test_plugin_render_single_full_item(self):
        """
        Full single item should build all HTML parts
        """
        # Create random values for parameters with a factory
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

        print()
        print(html)

        # Slider title
        self.assertInHTML(
            """<p class="slider__title">{}</p>""".format(
                slider.title
            ),
            html
        )

        # Item image and title
        pattern = (
            r'<div class="slider__item" style="background-image\: url\(/media/cache/.*\.jpg.*>'
            r'<p class="slider__item-title">{title:s}</p>'
        ).format(
            title=item.title,
        )
        self.assertIsNotNone(re.search(pattern, html))

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        # Item content
        self.assertInHTML(
            """<div class="slider__item-content">{}</div>""".format(
                item.content
            ),
            html
        )

        link_template = (
            """<p class="slider__item-link">"""
            """<a class="button" href="{url}" target="blank">"""
            """{name}"""
            """</a>"""
            """</p>"""
        )
        self.assertInHTML(
            link_template.format(
                name=item.link_name,
                url=item.link_url,
            ),
            html
        )

    def test_plugin_render_no_item_content(self):
        """
        When item content is empty, its HTML part should not be present
        """
        # Create random values for parameters with a factory
        slider = SliderFactory()
        item = SlideItemFactory.create(
            slider=slider,
            content="",
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            SliderPlugin,
            copy_relations_from=slider,
            template=slider.template,
            title=slider.title,
        )

        print()
        print(html)

        pattern = (
            r'<div class="slider__item-content">'
        )
        self.assertIsNone(re.search(pattern, html))

    def test_plugin_render_many_item(self):
        """
        When slider has many item, every item titles should be here
        """
        # Create random values for parameters with a factory
        slider = SliderFactory.create()

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

        #print()
        #print(html)

        # Item titles
        self.assertInHTML(
            """<p class="slider__item-title">{}</p>""".format(
                item_first.title
            ),
            html
        )

        self.assertInHTML(
            """<p class="slider__item-title">{}</p>""".format(
                item_second.title
            ),
            html
        )

    def test_plugin_queryset_items_order(self):
        """
        Item order should be respected
        """
        slider = SliderFactory.create()

        # Create item in various order
        item_third = SlideItemFactory.create(slider=slider, order=3, title="3")
        item_first = SlideItemFactory.create(slider=slider, order=1, title="1")
        item_second = SlideItemFactory.create(slider=slider, order=2, title="2")
        item_fourth = SlideItemFactory.create(slider=slider, order=4, title="4")

        # Build plugin
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder,
            SliderPlugin,
            "en",
            template=slider.template,
            title=slider.title,
        )
        model_instance.copy_relations(slider)

        # Get the ressources queryset from plugin render context
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        items = [(item.title, item.order) for item in context["slides"]]

        assert items == [('1', 1), ('2', 2), ('3', 3), ('4', 4)]

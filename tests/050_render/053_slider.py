import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.plugins.slider import SliderPlugin
from cmsplugin_blocks.factories.slider import SliderFactory, SlideItemFactory


class SliderRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Slider plugin render tests case"""

    def test_empty(self):
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

    def test_single_full_item(self):
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
            r'<div class="slider__item" style="background-image\: url\(/media/cache/.*\.png.*>'
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
            """<a class="button" href="{url}" target="_blank">"""
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

    def test_no_item_content(self):
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

    def test_many_item(self):
        """
        When slider has many item, every item titles should be here
        """
        # Create random values for parameters with a factory
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

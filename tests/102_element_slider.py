import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cms.api import create_page, add_plugin
from cms.models import Placeholder
from cms.utils.urlutils import admin_reverse

from cmsplugin_blocks.choices_helpers import get_slider_default_template
from cmsplugin_blocks.models import Slider
from cmsplugin_blocks.cms_plugins import SliderPlugin
from cmsplugin_blocks.factories.slider import SliderFactory, SlideItemFactory
from cmsplugin_blocks.factories.user import UserFactory


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

    def test_plugin_queryset_items_order(self):
        """
        Item order should be respected
        """
        slider = SliderFactory()

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

    def test_slider_plugin_form_view_add(self):
        """
        Plugin creation form should return a success status code and every
        expected field should be present in HTML.
        """
        # Connect a dummy admin
        staff = UserFactory(is_staff=True, is_superuser=True)
        self.client.login(username=staff.username, password="password")

        # Create dummy page
        page = create_page(
            language="en",
            title="Dummy",
            slug="dummy",
            template="pages/default.html",
        )

        # Get placeholder
        placeholder = page.placeholders.get(slot="content")

        # Get the edition plugin form url and open it
        url = admin_reverse('cms_page_add_plugin')
        response = self.client.get(url, {
            'plugin_type': 'SliderPlugin',
            'placeholder_id': placeholder.pk,
            'target_language': 'en',
            'plugin_language': 'en',
        })

        html = response.content.decode("utf-8")

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Check all expected fields are present
        self.assertIsNotNone(
            re.search(
                (
                    r'<select.*id="id_template".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="text.*id="id_title".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="file.*id="id_slide_item-__prefix__-image".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<textarea.*id="id_slide_item-__prefix__-content".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="number.*id="id_slide_item-__prefix__-order".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="text.*id="id_slide_item-__prefix__-link_name".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="text.*id="id_slide_item-__prefix__-link_url".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="checkbox.*id="id_slide_item-__prefix__-link_open_blank".*>'
                ),
                html
            )
        )

    def test_slider_plugin_form_view_edit(self):
        """
        Plugin edition form should return a success status code and every
        expected field should be present in HTML.
        """
        # Create random values for parameters with a factory
        slider = SliderFactory()
        item = SlideItemFactory.create(
            slider=slider,
        )

        # Connect a dummy admin
        staff = UserFactory(is_staff=True, is_superuser=True)
        self.client.login(username=staff.username, password="password")

        # Create dummy page
        page = create_page(
            language="en",
            title="Dummy",
            slug="dummy",
            template="pages/default.html",
        )

        # Add slider plugin to placeholder
        placeholder = page.placeholders.get(slot="content")
        model_instance = add_plugin(
            placeholder,
            SliderPlugin,
            "en",
            template=slider.template,
            title=slider.title,
        )
        model_instance.copy_relations(slider)

        # Get the edition plugin form url and open it
        url = admin_reverse('cms_page_edit_plugin', args=[model_instance.id])
        response = self.client.get(url)

        html = response.content.decode("utf-8")

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Check expected slider fields are present
        self.assertIsNotNone(
            re.search(
                (
                    r'<select.*id="id_template".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="text.*id="id_title".*>'
                ),
                html
            )
        )
        # Check only a single expected empty field
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="file.*id="id_slide_item-__prefix__-image".*>'
                ),
                html
            )
        )
        # Check only a single expected filled field
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="file.*id="id_slide_item-0-image".*>'
                ),
                html
            )
        )

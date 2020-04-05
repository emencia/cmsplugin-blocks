import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cms.api import create_page, add_plugin
from cms.models import Placeholder
from cms.utils.urlutils import admin_reverse

from cmsplugin_blocks.plugins.slider import SliderPlugin
from cmsplugin_blocks.factories.slider import SliderFactory, SlideItemFactory
from cmsplugin_blocks.factories.user import UserFactory


class SliderCMSPluginsTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Slider plugin tests case"""

    def test_queryset_items_order(self):
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

    def test_form_view_add(self):
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

    def test_form_view_edit(self):
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

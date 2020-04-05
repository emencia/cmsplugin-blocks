import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cms.api import create_page, add_plugin
from cms.models import Placeholder
from cms.utils.urlutils import admin_reverse

from cmsplugin_blocks.plugins.album import AlbumPlugin
from cmsplugin_blocks.factories.album import AlbumFactory, AlbumItemFactory
from cmsplugin_blocks.factories.user import UserFactory


class AlbumCMSPluginsTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Album plugin tests case"""

    def test_queryset_items_order(self):
        """
        Item order should be respected
        """
        album = AlbumFactory()

        # Create item in various order
        item_third = AlbumItemFactory.create(album=album, order=3, title="3")
        item_first = AlbumItemFactory.create(album=album, order=1, title="1")
        item_second = AlbumItemFactory.create(album=album, order=2, title="2")
        item_fourth = AlbumItemFactory.create(album=album, order=4, title="4")

        # Build plugin
        placeholder = Placeholder.objects.create(slot="test")
        model_instance = add_plugin(
            placeholder,
            AlbumPlugin,
            "en",
            template=album.template,
            title=album.title,
        )
        model_instance.copy_relations(album)

        # Get the ressources queryset from plugin render context
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        items = [(item.title, item.order) for item in context["ressources"]]

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
            'plugin_type': 'AlbumPlugin',
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
                    r'<input.*type="text.*id="id_album_item-__prefix__-title".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="number.*id="id_album_item-__prefix__-order".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="file.*id="id_album_item-__prefix__-image".*>'
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
        album = AlbumFactory()
        item = AlbumItemFactory.create(
            album=album,
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

        # Add album plugin to placeholder
        placeholder = page.placeholders.get(slot="content")
        model_instance = add_plugin(
            placeholder,
            AlbumPlugin,
            "en",
            template=album.template,
            title=album.title,
        )
        model_instance.copy_relations(album)

        # Get the edition plugin form url and open it
        url = admin_reverse('cms_page_edit_plugin', args=[model_instance.id])
        response = self.client.get(url)

        html = response.content.decode("utf-8")
        print(html)

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Check expected album fields are present
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
                    r'<input.*type="file.*id="id_album_item-__prefix__-image".*>'
                ),
                html
            )
        )
        # Check only a single expected filled field
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="file.*id="id_album_item-0-image".*>'
                ),
                html
            )
        )

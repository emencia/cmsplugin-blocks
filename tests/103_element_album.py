import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cms.api import create_page, add_plugin
from cms.models import Placeholder
from cms.utils.urlutils import admin_reverse

from cmsplugin_blocks.choices_helpers import get_album_default_template
from cmsplugin_blocks.models import Album
from cmsplugin_blocks.cms_plugins import AlbumPlugin
from cmsplugin_blocks.factories.album import AlbumFactory, AlbumItemFactory
from cmsplugin_blocks.factories.user import UserFactory


def test_factory(db):
    """
    Factory should correctly create a new plugin object without any errors
    """
    instance = AlbumFactory()
    assert instance.template == get_album_default_template()

    instance = AlbumFactory(template="foo")
    assert instance.template == "foo"


def test_model_str(db, settings):
    """
    Model str should be correct in any case and truncated to 4 words with
    stripped HTML.
    """
    # Default filling from factory
    instance = AlbumFactory()
    assert len(str(instance)) > 0

    # Empty content
    instance = AlbumFactory(title="")
    assert len(str(instance)) == 0

    # Content with HTML and unicode
    instance = AlbumFactory(
        title=(
            """Lorem ipsum"""
        )
    )
    assert str(instance) == "Lorem ipsum"


class AlbumCMSPluginsTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Album plugin tests case"""

    def test_plugin_render_empty(self):
        """
        When there is no item, there should not be any HTML item part
        """
        # Create random values for parameters with a factory
        album = AlbumFactory(title="Lorem ipsum dolore")

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            template=album.template,
            title=album.title,
        )

        expected_title = """<p class="album__title">{}</p>""".format(
            album.title
        )
        self.assertInHTML(expected_title, html)

        expected_empty_items = """<div class="album__items"></div>"""
        self.assertInHTML(expected_empty_items, html)

    def test_plugin_render_single_full_item(self):
        """
        Plugin render with a album with a single item
        """
        # Create random values for parameters with a factory
        album = AlbumFactory()
        item = AlbumItemFactory.create(
            album=album,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=album,
            template=album.template,
            title=album.title,
        )

        print()
        print(html)

        # Album title
        self.assertInHTML(
            """<p class="album__title">{}</p>""".format(
                album.title
            ),
            html
        )

        # Item image and title
        pattern = (
            r'<a href="/media/blocks/album/.*\.jpg.*target="blank">'
            r'<img src="/media/cache/.*\.jpg.*alt="">'
            r'</a>'
        ).format(
            title=item.title,
        )
        self.assertIsNotNone(re.search(pattern, html))

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        # Item title
        self.assertInHTML(
            """<p class="album__item-title">{}</p>""".format(
                item.title
            ),
            html
        )

    def test_plugin_render_single_no_title(self):
        """
        Plugin render with a album with a single item without a title
        """
        # Create random values for parameters with a factory
        album = AlbumFactory()
        item = AlbumItemFactory.create(
            album=album,
            title="",
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=album,
            template=album.template,
            title=album.title,
        )

        print()
        print(html)

        pattern = (
            r'<p class="album__item-title">'
        )
        self.assertIsNone(re.search(pattern, html))

    def test_plugin_render_many_item(self):
        """
        Plugin render with a album with many various item
        """
        # Create random values for parameters with a factory
        album = AlbumFactory()

        item_1 = AlbumItemFactory.create(
            album=album,
        )
        item_2 = AlbumItemFactory.create(
            album=album,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=album,
            template=album.template,
            title=album.title,
        )

        #print()
        #print("album:", (album.id, album.title))
        #albums = album.slide_item.all()
        #print("album.slide_item.all:", albums)
        #if albums.count() > 0:
            #print([(item.id, item.album.title, item.album) for item in albums])

        #print()
        #print(html)

        # Item titles
        self.assertInHTML(
            """<p class="album__item-title">{}</p>""".format(
                item_1.title
            ),
            html
        )

        self.assertInHTML(
            """<p class="album__item-title">{}</p>""".format(
                item_2.title
            ),
            html
        )

    def test_plugin_queryset_items_order(self):
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

    def test_album_plugin_form_view_add(self):
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

    def test_album_plugin_form_view_edit(self):
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

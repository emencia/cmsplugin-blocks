import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cms.api import add_plugin
from cms.models import Placeholder

from cmsplugin_blocks.choices_helpers import get_album_default_template
from cmsplugin_blocks.models import Album
from cmsplugin_blocks.cms_plugins import AlbumPlugin
from cmsplugin_blocks.factories.album import AlbumFactory, AlbumItemFactory


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
        fabricated = AlbumFactory(title="Lorem ipsum dolore")

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            template=fabricated.template,
            title=fabricated.title,
        )

        expected_title = """<p class="album__title">{}</p>""".format(
            fabricated.title
        )
        self.assertInHTML(expected_title, html)

        expected_empty_items = """<div class="album__items"></div>"""
        self.assertInHTML(expected_empty_items, html)

    def test_plugin_render_single_full_item(self):
        """
        Plugin render with a album with a single item
        """
        # Create random values for parameters with a factory
        fabricated_album = AlbumFactory.create()
        fabricated_item = AlbumItemFactory.create(
            album=fabricated_album,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=fabricated_album,
            template=fabricated_album.template,
            title=fabricated_album.title,
        )

        print()
        print(html)

        # Album title
        self.assertInHTML(
            """<p class="album__title">{}</p>""".format(
                fabricated_album.title
            ),
            html
        )

        # Item image and title
        pattern = (
            r'<a href="/media/blocks/album/.*\.jpg.*target="blank">'
            r'<img src="/media/cache/.*\.jpg.*alt="">'
            r'</a>'
        ).format(
            title=fabricated_item.title,
        )
        self.assertIsNotNone(re.search(pattern, html))

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        # Item title
        self.assertInHTML(
            """<p class="album__item-title">{}</p>""".format(
                fabricated_item.title
            ),
            html
        )

    def test_plugin_render_single_no_title(self):
        """
        Plugin render with a album with a single item without a title
        """
        # Create random values for parameters with a factory
        fabricated_album = AlbumFactory.create()
        fabricated_item = AlbumItemFactory.create(
            album=fabricated_album,
            title="",
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=fabricated_album,
            template=fabricated_album.template,
            title=fabricated_album.title,
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
        fabricated_album = AlbumFactory.create()

        fabricated_item_1 = AlbumItemFactory.create(
            album=fabricated_album,
        )
        fabricated_item_2 = AlbumItemFactory.create(
            album=fabricated_album,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=fabricated_album,
            template=fabricated_album.template,
            title=fabricated_album.title,
        )

        #print()
        #print("album:", (fabricated_album.id, fabricated_album.title))
        #fabricated_albums = fabricated_album.slide_item.all()
        #print("fabricated_album.slide_item.all:", fabricated_albums)
        #if fabricated_albums.count() > 0:
            #print([(item.id, item.album.title, item.album) for item in fabricated_albums])

        #print()
        #print(html)

        # Item titles
        self.assertInHTML(
            """<p class="album__item-title">{}</p>""".format(
                fabricated_item_1.title
            ),
            html
        )

        self.assertInHTML(
            """<p class="album__item-title">{}</p>""".format(
                fabricated_item_2.title
            ),
            html
        )

    def test_plugin_queryset_items_order(self):
        """
        Item order should be respected
        """
        album = AlbumFactory.create()

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

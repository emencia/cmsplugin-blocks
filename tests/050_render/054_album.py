import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.plugins.album import AlbumPlugin
from cmsplugin_blocks.factories.album import AlbumFactory, AlbumItemFactory


class AlbumRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Album plugin render tests case"""

    def test_empty(self):
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

    def test_single_full_item(self):
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
            r'<a href="/media/blocks/album/.*\.png.*target="blank">'
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

    def test_single_no_title(self):
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

    def test_many_item(self):
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

import logging

from cmsplugin_blocks.cms_plugins import AlbumPlugin
from cmsplugin_blocks.factories import AlbumFactory, AlbumItemFactory
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase
from cmsplugin_blocks.utils.tests import html_pyquery

from tests.utils import FixturesTestCaseMixin


class AlbumRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Album plugin render tests case
    """

    def test_empty(self):
        """
        When there is no item, there should not be any HTML item part
        """
        album = AlbumFactory(title="Lorem ipsum dolore")

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            template=album.template,
            title=album.title,
        )

        # Parse resulting plugin HTML render
        dom = html_pyquery(html)

        # Check title
        album_title = dom.find(".album__title")
        assert len(album_title) == 1
        assert album_title[0].text.strip() == album.title

        album_items = dom.find(".album__item")
        assert len(album_items) == 0

    def test_single_full_item(self):
        """
        Plugin render with a album with a single item
        """
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

        dom = html_pyquery(html)

        # Check title
        album_title = dom.find(".album__title")
        assert len(album_title) == 1
        assert album_title[0].text.strip() == album.title

        # Item image and title
        album_item = dom.find(".album__item")[0]
        item_image_url = album_item[0].cssselect("img")[0].get("src")
        assert item_image_url.startswith("/media/cache/") is True
        item_link = album_item.cssselect("a")[0]
        assert item_link.get("href").startswith("/media/blocks/albumitem/")

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        item_title = album_item.cssselect(".album__item-title")[0]
        assert item_title.text.strip() == item.title

    def test_single_no_title(self):
        """
        Plugin render with a album with a single item without a title
        """
        album = AlbumFactory()
        AlbumItemFactory.create(
            album=album,
            title="",
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=album,
            template=album.template,
            title=album.title,
        )

        dom = html_pyquery(html)

        item_content = dom.find(".album__item-title")
        assert len(item_content) == 0

    def test_many_item(self):
        """
        Plugin render with a album with many various item
        """
        album = AlbumFactory()

        item_first = AlbumItemFactory.create(
            album=album,
        )
        item_second = AlbumItemFactory.create(
            album=album,
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            AlbumPlugin,
            copy_relations_from=album,
            template=album.template,
            title=album.title,
        )

        dom = html_pyquery(html)

        # Item titles
        item_titles = dom.find(".album__item-title")
        assert len(item_titles) == 2
        assert item_titles[0].text.strip() == item_first.title
        assert item_titles[1].text.strip() == item_second.title

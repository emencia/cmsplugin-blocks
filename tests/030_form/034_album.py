import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.factories.album import AlbumFactory, AlbumItemFactory
from cmsplugin_blocks.forms.album import AlbumForm, AlbumItemForm


class AlbumFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Album form tests case"""

    def test_album_empty(self):
        """
        Container form should not be valid with missing required fields.
        """
        form = AlbumForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("template", form.errors)
        self.assertEqual(len(form.errors), 2)

    def test_item_empty(self):
        """
        Item form should not be valid with missing required fields.
        """
        form = AlbumItemForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("album", form.errors)
        self.assertIn("order", form.errors)
        self.assertIn("image", form.errors)
        self.assertEqual(len(form.errors), 3)

    def test_album_success(self):
        """
        Form should be valid with factory datas.
        """
        album = AlbumFactory()

        form = AlbumForm({
            "title": album.title,
            "template": album.template,
        })
        self.assertTrue(form.is_valid())

        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.title, album.title)
        self.assertEqual(instance.template, album.template)

    def test_item_success(self):
        """
        Item form should be valid with factory datas.
        """
        album = AlbumFactory()
        item = AlbumItemFactory(album=album)

        form = AlbumItemForm({
            "album": item.album,
            "order": item.order,
        }, {
            "image": item.image,
        })
        self.assertTrue(form.is_valid())

        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.album, album)
        self.assertEqual(instance.order, item.order)
        self.assertEqual(instance.image, item.image)

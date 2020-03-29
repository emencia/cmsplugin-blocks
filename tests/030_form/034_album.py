import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.factories.album import AlbumFactory, AlbumItemFactory
from cmsplugin_blocks.forms.album import AlbumForm, AlbumItemForm


class AlbumFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Album form tests case"""

    def test_container_empty(self):
        """
        Container form should not be valid with missing required fields.
        """
        form = AlbumForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("template", form.errors)

    def test_item_empty(self):
        """
        Item form should not be valid with missing required fields.
        """
        form = AlbumItemForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("album", form.errors)
        self.assertIn("order", form.errors)
        self.assertIn("image", form.errors)

    def test_container_success(self):
        """
        Form should be valid with factory datas.
        """
        album = AlbumFactory()

        form = AlbumForm({
            "title": album.title,
            "template": album.template,
        })
        self.assertTrue(form.is_valid())

        album_instance = form.save()

        # Checked save values are the same from factory
        self.assertEqual(album_instance.title, album.title)
        self.assertEqual(album_instance.template, album.template)

import io
import os

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from cmsplugin_blocks.factories import AlbumFactory, AlbumItemFactory
from cmsplugin_blocks.forms import AlbumForm, AlbumItemForm
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase

from tests.utils import FixturesTestCaseMixin


class AlbumFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Album form tests case
    """

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
            "features": album.features,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.title, album.title)
        self.assertEqual(instance.features, album.features)
        self.assertEqual(instance.template, album.template)

    @override_settings(BLOCKS_ALBUM_FEATURES=[])
    def test_album_empty_feature_choices(self):
        """
        When feature choices are empty, form should still continue to work correctly.
        """
        album = AlbumFactory()

        form = AlbumForm({
            "title": album.title,
            "template": album.template,
            "features": album.features,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Ensure test runned with empty choices
        self.assertEqual(instance.features, [])

        # Checked saved values are the same from factory
        self.assertEqual(instance.title, album.title)
        self.assertEqual(instance.features, album.features)
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
            "features": item.features,
        }, {
            "image": item.image,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.album, album)
        self.assertEqual(instance.features, item.features)
        self.assertEqual(instance.order, item.order)
        self.assertEqual(instance.image, item.image)

    @override_settings(BLOCKS_ALBUMITEM_FEATURES=[])
    def test_item_empty_feature_choices(self):
        """
        When feature choices are empty, form should still continue to work correctly.
        """
        album = AlbumFactory()
        item = AlbumItemFactory(album=album)

        form = AlbumItemForm({
            "album": item.album,
            "order": item.order,
            "features": item.features,
        }, {
            "image": item.image,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Ensure test runned with empty choices
        self.assertEqual(instance.features, [])

        # Checked saved values are the same from factory
        self.assertEqual(instance.album, album)
        self.assertEqual(instance.features, item.features)
        self.assertEqual(instance.order, item.order)
        self.assertEqual(instance.image, item.image)

    def test_mass_upload_success(self):
        """
        When "mass_upload" field is filled with a valid ZIP file, form save
        should fill the Album attribute ``_awaiting_items`` with AlbumItem
        instances for each valid image file from ZIP archive.
        """
        album = AlbumFactory()

        filepath = os.path.join(
            self._tests_settings.fixtures_path,
            "zip_samples",
            "basic.zip"
        )

        with io.open(filepath, "rb") as fp:
            _archive = SimpleUploadedFile(
                "basic.zip",
                fp.read(),
                content_type="application/zip"
            )

        form = AlbumForm({
            "title": album.title,
            "template": album.template,
        }, {
            "mass_upload": _archive,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Expected item counter
        self.assertEqual(len(instance._awaiting_items), 4)

        # Check expected item without image file since saved file path may
        # contain a random hash we don't know yet
        def item_matrix(v):
            return {
                "id": v.id,
                "title": v.title,
                "order": 0,
            }

        result_items = [item_matrix(item) for item in instance._awaiting_items]
        expected_items = [
            {"id": None, "title": "basic/107x107.png", "order": 0},
            {"id": None, "title": "basic/120x100.jpg", "order": 0},
            {"id": None, "title": "basic/120x100.png", "order": 0},
            {"id": None, "title": "basic/120x120.png", "order": 0},
        ]

        self.assertEqual(result_items, expected_items)

        # For sanity check the image file attribute is not empty and is an
        # image file (simply assumed from file extension)
        for item in instance._awaiting_items:
            self.assertIsNotNone(item.image)
            self.assertTrue((item.image.url.endswith(".jpg")
                             or item.image.url.endswith(".png")))

    def test_mass_upload_fail(self):
        """
        When "mass_upload" field is filled with an invalid ZIP file, form error
        should be present about invalid field and an exception should be raised
        when trying to save.
        """
        album = AlbumFactory()

        filepath = os.path.join(
            self._tests_settings.fixtures_path,
            "zip_samples",
            "truncated.zip"
        )

        with io.open(filepath, "rb") as fp:
            _archive = SimpleUploadedFile(
                "truncated.zip",
                fp.read(),
                content_type="application/zip"
            )

        form = AlbumForm({
            "title": album.title,
            "template": album.template,
        }, {
            "mass_upload": _archive,
        })

        self.assertFalse(form.is_valid())
        self.assertIn("mass_upload", form.errors)
        self.assertEqual(len(form.errors), 1)

        with pytest.raises(ValueError):
            form.save()

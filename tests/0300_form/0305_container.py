from django.test import override_settings

from cmsplugin_blocks.factories import ContainerFactory
from cmsplugin_blocks.forms import ContainerForm
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase

from tests.utils import FixturesTestCaseMixin


class ContainerFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Container form tests case
    """
    def test_empty(self):
        """
        Form should not be valid with missing required fields.
        """
        form = ContainerForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("template", form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_success(self):
        """
        Form should be valid with factory datas.
        """
        container = ContainerFactory()

        form = ContainerForm({
            "template": container.template,
            "features": container.features,
            "image": container.image,
            "content": container.content,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Checked saved values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(instance.template, container.template)
        self.assertEqual(instance.features, container.features)
        self.assertEqual(instance.content, container.content)

    @override_settings(BLOCKS_CONTAINER_FEATURES=[])
    def test_empty_feature_choices(self):
        """
        When feature choices are empty, form should still continue to work correctly.
        """
        container = ContainerFactory()

        form = ContainerForm({
            "template": container.template,
            "features": container.features,
            "image": container.image,
            "content": container.content,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Ensure test runned with empty choices
        self.assertEqual(instance.features, [])

        # Checked saved values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(instance.template, container.template)
        self.assertEqual(instance.features, container.features)
        self.assertEqual(instance.content, container.content)

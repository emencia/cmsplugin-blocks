from django.test import override_settings

from cmsplugin_blocks.factories import CardFactory
from cmsplugin_blocks.forms import CardForm
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase

from tests.utils import FixturesTestCaseMixin


class CardFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Card form tests case
    """
    def test_empty(self):
        """
        Form should not be valid with missing required fields.
        """
        form = CardForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("template", form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_success(self):
        """
        Form should be valid with factory datas.
        """
        card = CardFactory()

        form = CardForm({
            "template": card.template,
            "features": card.features,
            "image": card.image,
            "content": card.content,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Checked saved values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(instance.template, card.template)
        self.assertEqual(instance.features, card.features)
        self.assertEqual(instance.content, card.content)

    @override_settings(BLOCKS_CARD_FEATURES=[])
    def test_empty_feature_choices(self):
        """
        When feature choices are empty, form should still continue to work correctly.
        """
        card = CardFactory()

        form = CardForm({
            "template": card.template,
            "features": card.features,
            "image": card.image,
            "content": card.content,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Ensure test runned with empty choices
        self.assertEqual(instance.features, [])

        # Checked saved values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(instance.template, card.template)
        self.assertEqual(instance.features, card.features)
        self.assertEqual(instance.content, card.content)

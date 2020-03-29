import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.factories.card import CardFactory
from cmsplugin_blocks.forms.card import CardForm


class CardFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Card form tests case"""
    def test_empty(self):
        """
        Form should not be valid with missing required fields.
        """
        form = CardForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("alignment", form.errors)
        self.assertIn("template", form.errors)

    def test_success(self):
        """
        Form should be valid with factory datas.
        """
        card = CardFactory()

        form = CardForm({
            "template": card.template,
            "alignment": card.alignment,
            "image": card.image,
            "content": card.content,
        })
        self.assertTrue(form.is_valid())

        card_instance = form.save()

        # Checked save values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(card_instance.template, card.template)
        self.assertEqual(card_instance.alignment, card.alignment)
        self.assertEqual(card_instance.content, card.content)

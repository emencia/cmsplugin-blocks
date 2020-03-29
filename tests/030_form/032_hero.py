import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.factories.hero import HeroFactory
from cmsplugin_blocks.forms.hero import HeroForm


class HeroFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Hero form tests case"""
    def test_empty(self):
        """
        Form should not be valid with missing required fields.
        """
        form = HeroForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("template", form.errors)

    def test_success(self):
        """
        Form should be valid with factory datas.
        """
        hero = HeroFactory()

        form = HeroForm({
            "template": hero.template,
            "image": hero.image,
            "content": hero.content,
        })
        self.assertTrue(form.is_valid())

        hero_instance = form.save()

        # Checked save values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(hero_instance.template, hero.template)
        self.assertEqual(hero_instance.content, hero.content)

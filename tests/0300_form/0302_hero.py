from django.test import override_settings

from cmsplugin_blocks.factories import HeroFactory
from cmsplugin_blocks.forms import HeroForm
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase

from tests.utils import FixturesTestCaseMixin


class HeroFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Hero form tests case
    """
    def test_empty(self):
        """
        Form should not be valid with missing required fields.
        """
        form = HeroForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("template", form.errors)
        self.assertIn("content", form.errors)
        self.assertEqual(len(form.errors), 2)

    def test_success(self):
        """
        Form should be valid with factory datas.
        """
        hero = HeroFactory()

        form = HeroForm({
            "template": hero.template,
            "features": hero.features,
            "image": hero.image,
            "content": hero.content,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Checked saved values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(instance.template, hero.template)
        self.assertEqual(instance.features, hero.features)
        self.assertEqual(instance.content, hero.content)

    @override_settings(BLOCKS_HERO_FEATURES=[])
    def test_empty_feature_choices(self):
        """
        When feature choices are empty, form should still continue to work correctly.
        """
        hero = HeroFactory()

        form = HeroForm({
            "template": hero.template,
            "features": hero.features,
            "image": hero.image,
            "content": hero.content,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Ensure test runned with empty choices
        self.assertEqual(instance.features, [])

        # Checked saved values are the same from factory, ignore the image to
        # avoid playing with file
        self.assertEqual(instance.template, hero.template)
        self.assertEqual(instance.features, hero.features)
        self.assertEqual(instance.content, hero.content)

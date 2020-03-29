import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.factories.slider import SliderFactory, SlideItemFactory
from cmsplugin_blocks.forms.slider import SliderForm, SlideItemForm


class SliderFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Slider form tests case"""

    def test_empty(self):
        """
        Container form should not be valid with missing required fields.
        """
        form = SliderForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("template", form.errors)

    def test_item_empty(self):
        """
        Item form should not be valid with missing required fields.
        """
        form = SlideItemForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("slider", form.errors)
        self.assertIn("order", form.errors)
        self.assertIn("image", form.errors)

    def test_container_success(self):
        """
        Form should be valid with factory datas.
        """
        slider = SliderFactory()

        form = SliderForm({
            "title": slider.title,
            "template": slider.template,
        })
        self.assertTrue(form.is_valid())

        slider_instance = form.save()

        # Checked save values are the same from factory
        self.assertEqual(slider_instance.title, slider.title)
        self.assertEqual(slider_instance.template, slider.template)

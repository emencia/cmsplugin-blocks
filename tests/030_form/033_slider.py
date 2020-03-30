import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.factories.slider import SliderFactory, SlideItemFactory
from cmsplugin_blocks.forms.slider import SliderForm, SlideItemForm


class SliderFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Slider form tests case"""

    def test_slider_empty(self):
        """
        Container form should not be valid with missing required fields.
        """
        form = SliderForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("template", form.errors)
        self.assertEqual(len(form.errors), 2)

    def test_item_empty(self):
        """
        Item form should not be valid with missing required fields.
        """
        form = SlideItemForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("slider", form.errors)
        self.assertIn("order", form.errors)
        self.assertIn("image", form.errors)
        self.assertEqual(len(form.errors), 3)

    def test_slider_success(self):
        """
        Form should be valid with factory datas.
        """
        slider = SliderFactory()

        form = SliderForm({
            "title": slider.title,
            "template": slider.template,
        })
        self.assertTrue(form.is_valid())

        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.title, slider.title)
        self.assertEqual(instance.template, slider.template)

    def test_item_success(self):
        """
        Item form should be valid with factory datas.
        """
        slider = SliderFactory()
        item = SlideItemFactory(slider=slider)

        form = SlideItemForm({
            "slider": item.slider,
            "order": item.order,
        }, {
            "image": item.image,
        })
        self.assertTrue(form.is_valid())

        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.slider, slider)
        self.assertEqual(instance.order, item.order)
        self.assertEqual(instance.image, item.image)

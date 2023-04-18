from django.test import override_settings

from cmsplugin_blocks.factories import SliderFactory, SlideItemFactory
from cmsplugin_blocks.forms import SliderForm, SlideItemForm
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase

from tests.utils import FixturesTestCaseMixin


class SliderFormTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Slider form tests case
    """

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
        self.assertIn("title", form.errors)
        self.assertIn("order", form.errors)
        self.assertIn("image", form.errors)
        self.assertEqual(len(form.errors), 4)

    def test_slider_success(self):
        """
        Form should be valid with factory datas.
        """
        slider = SliderFactory()

        form = SliderForm({
            "title": slider.title,
            "template": slider.template,
            "features": slider.features,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.title, slider.title)
        self.assertEqual(instance.features, slider.features)
        self.assertEqual(instance.template, slider.template)

    @override_settings(BLOCKS_SLIDER_FEATURES=[])
    def test_slider_empty_feature_choices(self):
        """
        When feature choices are empty, form should still continue to work correctly.
        """
        slider = SliderFactory()

        form = SliderForm({
            "title": slider.title,
            "template": slider.template,
            "features": slider.features,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Ensure test runned with empty choices
        self.assertEqual(instance.features, [])

        # Checked saved values are the same from factory
        self.assertEqual(instance.title, slider.title)
        self.assertEqual(instance.features, slider.features)
        self.assertEqual(instance.template, slider.template)

    def test_item_success(self):
        """
        Item form should be valid with factory datas.
        """
        slider = SliderFactory()
        item = SlideItemFactory(slider=slider)

        form = SlideItemForm({
            "slider": item.slider,
            "title": item.title,
            "order": item.order,
            "features": item.features,
        }, {
            "image": item.image,
        })

        self.assertTrue(form.is_valid())
        instance = form.save()

        # Checked saved values are the same from factory
        self.assertEqual(instance.slider, slider)
        self.assertEqual(instance.order, item.order)
        self.assertEqual(instance.features, item.features)
        self.assertEqual(instance.image, item.image)

    @override_settings(BLOCKS_SLIDERITEM_FEATURES=[])
    def test_item_empty_feature_choices(self):
        """
        When feature choices are empty, form should still continue to work correctly.
        """
        slider = SliderFactory()
        item = SlideItemFactory(slider=slider)

        form = SlideItemForm({
            "slider": item.slider,
            "title": item.title,
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
        self.assertEqual(instance.slider, slider)
        self.assertEqual(instance.order, item.order)
        self.assertEqual(instance.features, item.features)
        self.assertEqual(instance.image, item.image)

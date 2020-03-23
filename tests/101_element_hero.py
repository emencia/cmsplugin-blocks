import logging
import re

import pytest

from cms.api import create_page, add_plugin
from cms.utils.urlutils import admin_reverse

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.choices_helpers import get_hero_default_template
from cmsplugin_blocks.cms_plugins import HeroPlugin
from cmsplugin_blocks.factories.hero import HeroFactory
from cmsplugin_blocks.factories.user import UserFactory
from cmsplugin_blocks.forms.hero import HeroForm


def test_factory(db):
    """
    Factory should correctly create a new plugin object without any errors
    """
    instance = HeroFactory()
    assert instance.template == get_hero_default_template()

    instance = HeroFactory(template="foo")
    assert instance.template == "foo"


def test_model_str(db, settings):
    """
    Model str should be correct in any case and truncated to 4 words with
    stripped HTML.
    """
    # Default filling from factory
    instance = HeroFactory()
    assert len(str(instance)) > 0

    # Empty content
    instance = HeroFactory(content="")
    assert len(str(instance)) == 0

    # Content with HTML and unicode
    instance = HeroFactory(
        content=(
            """<p>"""
            """Lorem ipsum <b>日本</b> and voilà!"""
            """</p>"""
        )
    )
    assert str(instance) == "Lorem ipsum 日本 and..."


class HeroCMSPluginsTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Hero plugin tests case"""

    def test_hero_plugin_render_full(self):
        """
        Every parts should be present when rendered
        """
        # Create random values for parameters with a factory
        fabricated = HeroFactory(content="<p>Lorem ipsum dolore</p>")

        placeholder, model_instance, context, html = self.create_basic_render(
            HeroPlugin,
            template=fabricated.template,
            image=fabricated.image,
            content=fabricated.content,
        )

        print()
        print(html)

        # Check image
        pattern = (
            r'<div class="hero__wrapper" style="background-image\: url\(/media/cache/.*\.jpg.*>'
        )
        self.assertIsNotNone(re.search(pattern, html))

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        # Check content
        expected_content = """<div class="hero__content">{}</div>""".format(
            fabricated.content
        )
        self.assertInHTML(expected_content, html)

    def test_hero_plugin_render_no_content(self):
        """
        When hero has no content, content part should not be rendered
        """
        # Create random values for parameters with a factory
        fabricated = HeroFactory(content="")

        placeholder, model_instance, context, html = self.create_basic_render(
            HeroPlugin,
            template=fabricated.template,
            image=fabricated.image,
            content=fabricated.content,
        )

        print()
        print(html)

        pattern = (
            r'<div class="hero__content">'
        )
        self.assertIsNone(re.search(pattern, html))

    def test_hero_plugin_render_no_image(self):
        """
        When hero has no image, image part should not be rendered
        """
        # Create random values for parameters with a factory
        fabricated = HeroFactory(image=None)

        placeholder, model_instance, context, html = self.create_basic_render(
            HeroPlugin,
            template=fabricated.template,
            image=fabricated.image,
            content=fabricated.content,
        )

        print()
        print(html)

        # Check image
        pattern = (
            r'<div class="hero__wrapper">'
        )
        self.assertIsNotNone(re.search(pattern, html))

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

    def test_hero_form_empty(self):
        """
        Form should not be valid with missing required fields.
        """
        form = HeroForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("template", form.errors)

    def test_hero_form_success(self):
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

    def test_hero_plugin_form_view_add(self):
        """
        Plugin creation form should return a success status code and every
        expected field should be present in HTML.
        """
        # Connect a dummy admin
        staff = UserFactory(is_staff=True, is_superuser=True)
        self.client.login(username=staff.username, password="password")

        # Create dummy page
        page = create_page(
            language="en",
            title="Dummy",
            slug="dummy",
            template="pages/default.html",
        )

        # Get placeholder
        placeholder = page.placeholders.get(slot="content")

        # Get the edition plugin form url and open it
        url = admin_reverse('cms_page_add_plugin')
        response = self.client.get(url, {
            'plugin_type': 'HeroPlugin',
            'placeholder_id': placeholder.pk,
            'target_language': 'en',
            'plugin_language': 'en',
        })

        html = response.content.decode("utf-8")

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Check all expected fields are present
        self.assertIsNotNone(
            re.search(
                (
                    r'<select.*id="id_template".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="file.*id="id_image".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<textarea.*id="id_content".*>'
                ),
                html
            )
        )

    def test_hero_plugin_form_view_edit(self):
        """
        Plugin edition form should return a success status code and every
        expected field should be present in HTML.
        """
        # Create random values for parameters with a factory
        hero = HeroFactory(content="<p>Lorem ipsum dolore</p>")

        # Connect a dummy admin
        staff = UserFactory(is_staff=True, is_superuser=True)
        self.client.login(username=staff.username, password="password")

        # Create dummy page
        page = create_page(
            language="en",
            title="Dummy",
            slug="dummy",
            template="pages/default.html",
        )

        # Add hero plugin to placeholder
        placeholder = page.placeholders.get(slot="content")
        model_instance = add_plugin(
            placeholder,
            HeroPlugin,
            "en",
            template=hero.template,
            image=hero.image,
            content=hero.content,
        )

        # Get the edition plugin form url and open it
        url = admin_reverse('cms_page_edit_plugin', args=[model_instance.id])
        response = self.client.get(url)

        html = response.content.decode("utf-8")

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Check all expected fields are present
        self.assertIsNotNone(
            re.search(
                (
                    r'<select.*id="id_template".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<input.*type="file.*id="id_image".*>'
                ),
                html
            )
        )
        self.assertIsNotNone(
            re.search(
                (
                    r'<textarea.*id="id_content".*>'
                ),
                html
            )
        )

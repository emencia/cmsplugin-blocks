import logging
import re

import pytest

from cms.api import create_page, add_plugin
from cms.utils.urlutils import admin_reverse

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.choices_helpers import get_card_default_template
from cmsplugin_blocks.cms_plugins import CardPlugin
from cmsplugin_blocks.factories.card import CardFactory
from cmsplugin_blocks.factories.user import UserFactory
from cmsplugin_blocks.forms.card import CardForm


def test_factory(db):
    """
    Factory should correctly create a new plugin object without any errors
    """
    instance = CardFactory()
    assert instance.template == get_card_default_template()

    instance = CardFactory(template="foo")
    assert instance.template == "foo"


def test_model_str(db, settings):
    """
    Model str should be correct in any case and truncated to 4 words with
    stripped HTML.
    """
    # Default filling from factory
    instance = CardFactory()
    assert len(str(instance)) > 0

    # Empty content
    instance = CardFactory(content="")
    assert len(str(instance)) == 0

    # Content with HTML and unicode
    instance = CardFactory(
        content=(
            """<p>"""
            """Lorem ipsum <b>日本</b> and voilà!"""
            """</p>"""
        )
    )
    assert str(instance) == "Lorem ipsum 日本 and..."


class CardCMSPluginsTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Card plugin tests case"""

    def test_card_plugin_render_full(self):
        """
        Every parts should be present when rendered
        """
        # Create random values for parameters with a factory
        card = CardFactory(content="<p>Lorem ipsum dolore</p>")

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            alignment=card.alignment,
            image=card.image,
            content=card.content,
        )

        print()
        print(html)

        # Check alignment
        pattern = (
            r'<div class="card card--{}">'
        ).format(
            card.alignment
        )
        self.assertIsNotNone(re.search(pattern, html))

        # Check image
        pattern = (
            r'<div class="card__media">'
            r'<img src="/media/cache/.*\.jpg.*alt="">'
            r'</div>'
        )
        self.assertIsNotNone(re.search(pattern, html))

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        expected_content = """<div class="card__content">{}</div>""".format(
            card.content
        )
        self.assertInHTML(expected_content, html)

    def test_card_plugin_render_no_image(self):
        """
        When card has no image, image part should not be rendered
        """
        # Create random values for parameters with a factory
        card = CardFactory(
            image=None
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            alignment=card.alignment,
            image=card.image,
            content=card.content,
        )

        print()
        print(html)

        # Check image
        pattern = (
            r'<div class="card__media">'
            r'<img src="/media/blocks/card/.*\.jpg.*alt="">'
            r'</div>'
        )
        self.assertIsNone(re.search(pattern, html))

        expected_content = """<div class="card__content">{}</div>""".format(
            card.content
        )
        self.assertInHTML(expected_content, html)

    def test_card_plugin_render_no_content(self):
        """
        When card has no content, content part should not be rendered
        """
        # Create random values for parameters with a factory
        card = CardFactory(
            content=""
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            alignment=card.alignment,
            image=card.image,
            content=card.content,
        )

        print()
        print(html)

        pattern = (
            r'<div class="card__content">'
        )
        self.assertIsNone(re.search(pattern, html))

    def test_card_form_empty(self):
        """
        Form should not be valid with missing required fields.
        """
        form = CardForm({})

        self.assertFalse(form.is_valid())
        self.assertIn("alignment", form.errors)
        self.assertIn("template", form.errors)

    def test_card_form_success(self):
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

    def test_card_plugin_form_view_add(self):
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
            'plugin_type': 'CardPlugin',
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
                    r'<select.*id="id_alignment".*>'
                ),
                html
            )
        )
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

    def test_card_plugin_form_view_edit(self):
        """
        Plugin edition form should return a success status code and every
        expected field should be present in HTML.
        """
        # Create random values for parameters with a factory
        card = CardFactory(content="<p>Lorem ipsum dolore</p>")

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

        # Add card plugin to placeholder
        placeholder = page.placeholders.get(slot="content")
        model_instance = add_plugin(
            placeholder,
            CardPlugin,
            "en",
            template=card.template,
            alignment=card.alignment,
            image=card.image,
            content=card.content,
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
                    r'<select.*id="id_alignment".*>'
                ),
                html
            )
        )
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

import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.choices_helpers import get_card_default_template
from cmsplugin_blocks.cms_plugins import CardPlugin
from cmsplugin_blocks.factories.card import CardFactory


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
        fabricated = CardFactory(content="<p>Lorem ipsum dolore</p>")

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=fabricated.template,
            alignment=fabricated.alignment,
            image=fabricated.image,
            content=fabricated.content,
        )

        print()
        print(html)

        # Check alignment
        pattern = (
            r'<div class="card card--{}">'
        ).format(
            fabricated.alignment
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
            fabricated.content
        )
        self.assertInHTML(expected_content, html)

    def test_card_plugin_render_no_image(self):
        """
        When card has no image, image part should not be rendered
        """
        # Create random values for parameters with a factory
        fabricated = CardFactory(
            image=None
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=fabricated.template,
            alignment=fabricated.alignment,
            image=fabricated.image,
            content=fabricated.content,
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
            fabricated.content
        )
        self.assertInHTML(expected_content, html)

    def test_card_plugin_render_no_content(self):
        """
        When card has no content, content part should not be rendered
        """
        # Create random values for parameters with a factory
        fabricated = CardFactory(
            content=""
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=fabricated.template,
            alignment=fabricated.alignment,
            image=fabricated.image,
            content=fabricated.content,
        )

        print()
        print(html)

        pattern = (
            r'<div class="card__content">'
        )
        self.assertIsNone(re.search(pattern, html))

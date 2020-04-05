import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.plugins.card import CardPlugin
from cmsplugin_blocks.factories.card import CardFactory


class CardRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Card plugin render tests case"""

    def test_full(self):
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

    def test_no_image(self):
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

    def test_no_content(self):
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

import logging
import re

import pytest

from tests.utils import FixturesTestCaseMixin, CMSPluginTestCase

from cmsplugin_blocks.plugins.hero import HeroPlugin
from cmsplugin_blocks.factories.hero import HeroFactory


class HeroRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """Hero plugin render tests case"""

    def test_full(self):
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

    def test_no_content(self):
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

    def test_no_image(self):
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

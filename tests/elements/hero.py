import re

import pytest

from tests.utils import CMSPluginTestCase

from cmsplugin_blocks.choices_helpers import get_hero_default_template
from cmsplugin_blocks.cms_plugins import HeroPlugin
from cmsplugin_blocks.factories.hero import HeroFactory


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


class HeroCMSPluginsTestCase(CMSPluginTestCase):
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
            r'<div class="hero__wrapper" style="background-image\: url\(/media/blocks/hero/.*\.jpg.*>'
        )
        self.assertIsNotNone(re.search(pattern, html))

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

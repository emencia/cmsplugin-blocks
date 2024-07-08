import logging

from cmsplugin_blocks.cms_plugins import HeroPlugin
from cmsplugin_blocks.factories import HeroFactory, FeatureFactory
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase
from cmsplugin_blocks.utils.tests import html_pyquery

from tests.utils import FixturesTestCaseMixin


class HeroRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Hero plugin render tests case
    """

    def test_full(self):
        """
        Every parts should be present when rendered
        """
        hero = HeroFactory(content="<p>Lorem ipsum dolore</p>")

        placeholder, model_instance, context, html = self.create_basic_render(
            HeroPlugin,
            template=hero.template,
            image=hero.image,
            content=hero.content,
            copy_relations_from=hero,
        )

        # Parse resulting plugin HTML render
        dom = html_pyquery(html)

        # Check image
        hero_wrapper = dom.find(".hero__wrapper")[0]
        expected = "background-image: url(/media/cache/"
        assert hero_wrapper.get("style").startswith(expected) is True

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        # Check content
        hero_content = dom.find(".hero__content p")[0]
        assert hero_content.text == "Lorem ipsum dolore"

    def test_feature_classes(self):
        """
        When hero has features, their classes should be in .hero 'class' attribute
        without duplicates.
        """
        feature_foo = FeatureFactory(
            value="foo",
            scope="size",
            plugins=["HeroMain", "AlbumMain"],
        )
        feature_bar = FeatureFactory(
            value="bar",
            scope="color",
            plugins=["HeroMain"]
        )
        feature_foobis = FeatureFactory(
            value="foo",
            scope="extra",
            plugins=["HeroMain", "AlbumMain"],
        )

        hero = HeroFactory(
            fill_size_features=[feature_foo],
            fill_color_features=[feature_bar],
            fill_extra_features=[feature_foobis],
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            HeroPlugin,
            template=hero.template,
            image=hero.image,
            content=hero.content,
            copy_relations_from=hero,
        )

        dom = html_pyquery(html)
        features_classnames = [
            item
            for item in dom.attr("class").split()
            if item != "hero"
        ]
        assert features_classnames == [
            "bar",
            "foo",
        ]

    def test_no_content(self):
        """
        When hero has no content, content part should not be rendered
        """
        hero = HeroFactory(content="")

        placeholder, model_instance, context, html = self.create_basic_render(
            HeroPlugin,
            template=hero.template,
            image=hero.image,
            content=hero.content,
        )

        dom = html_pyquery(html)

        # Check content
        assert len(dom.find(".hero__content")) == 0

    def test_no_image(self):
        """
        When hero has no image, image part should not be rendered
        """
        hero = HeroFactory(image=None)

        placeholder, model_instance, context, html = self.create_basic_render(
            HeroPlugin,
            template=hero.template,
            image=hero.image,
            content=hero.content,
        )

        dom = html_pyquery(html)

        # Check image
        hero_wrapper = dom.find(".hero__wrapper")[0]
        assert hero_wrapper.get("style") is None

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

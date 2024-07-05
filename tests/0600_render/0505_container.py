import logging

from cmsplugin_blocks.cms_plugins import CardPlugin, ContainerPlugin, HeroPlugin
from cmsplugin_blocks.factories import CardFactory, ContainerFactory, HeroFactory
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase
from cmsplugin_blocks.utils.tests import html_pyquery

from tests.utils import FixturesTestCaseMixin


class ContainerRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Container plugin render tests case
    """

    def test_full(self):
        """
        Every parts should be present when rendered
        """
        container = ContainerFactory(content="<p>Lorem ipsum dolore</p>")

        placeholder, model_instance, context, html = self.create_basic_render(
            ContainerPlugin,
            title=container.title,
            template=container.template,
            features=container.features,
            image=container.image,
            content=container.content,
        )

        # Parse resulting plugin HTML render
        dom = html_pyquery(html)

        # Check title
        container_title = dom.find(".container__title")
        assert len(container_title) == 1
        assert container_title[0].text == container.title

        # Check image
        container_media = dom.find(".container__media")
        assert len(container_media) == 1

        container_image_url = container_media[0].cssselect("img")[0].get("src")
        assert container_image_url.startswith("/media/cache/") is True

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        # Check content
        container_content = dom.find(".container__content p")
        assert len(container_content) == 1
        assert container_content[0].text == "Lorem ipsum dolore"

    def test_no_image(self):
        """
        When container has no image, image part should not be rendered
        """
        container = ContainerFactory(image=None)

        placeholder, model_instance, context, html = self.create_basic_render(
            ContainerPlugin,
            template=container.template,
            features=container.features,
            image=container.image,
            content=container.content,
        )

        dom = html_pyquery(html)

        # Check image
        container_media = dom.find(".container__media")
        assert len(container_media) == 0

        # Check content
        container_content = dom.find(".container__content")
        assert len(container_content) == 1
        assert container_content[0].text == container.content

    def test_no_content(self):
        """
        When container has no content, content part should not be rendered
        """
        container = ContainerFactory(
            content=""
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            ContainerPlugin,
            template=container.template,
            image=container.image,
            content=container.content,
        )

        dom = html_pyquery(html)

        container_content = dom.find(".container__content")
        assert len(container_content) == 0

    def test_feature_classes(self):
        """
        When container has features, their classes should be in .container 'class'
        attribute without duplicates.
        """
        container = ContainerFactory(
            features=["foo", "blob", "foo"]
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            ContainerPlugin,
            template=container.template,
            image=container.image,
            content=container.content,
            features=container.features,
        )

        dom = html_pyquery(html)

        assert ["foo", "blob"] == [
            item
            for item in dom.attr("class").split()
            if item != "container"
        ]

    def test_children(self):
        """
        When container has plugin children, they should be rendered also.
        """
        card = CardFactory(image=None)
        container = ContainerFactory(image=None)
        hero = HeroFactory(image=None)

        placeholder, model_instance, context, html = self.create_basic_render(
            ContainerPlugin,
            template=container.template,
            title=container.title,
            features=container.features,
            children=[
                (
                    CardPlugin,
                    {
                        "title": card.title,
                        "template": card.template,
                    }
                ),
                (
                    HeroPlugin,
                    {
                        "template": hero.template,
                        "features": hero.features,
                        "content": hero.content,
                    }
                ),
            ],
        )

        dom = html_pyquery(html)

        children_card_title = dom.find(".container__items .card .card__title")
        assert len(children_card_title) == 1
        assert children_card_title[0].text == card.title

        children_hero_content = dom.find(".container__items .hero .hero__content")
        assert len(children_hero_content) == 1
        assert children_hero_content[0].text == hero.content

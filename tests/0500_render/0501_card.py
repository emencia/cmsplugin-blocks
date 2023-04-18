import logging

from cmsplugin_blocks.cms_plugins import CardPlugin
from cmsplugin_blocks.factories import CardFactory
from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase
from cmsplugin_blocks.utils.tests import html_pyquery

from tests.utils import FixturesTestCaseMixin


class CardRenderTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Card plugin render tests case
    """

    def test_full(self):
        """
        Every parts should be present when rendered
        """
        card = CardFactory(content="<p>Lorem ipsum dolore</p>")

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            title=card.title,
            template=card.template,
            features=card.features,
            image=card.image,
            content=card.content,
        )

        # Parse resulting plugin HTML render
        dom = html_pyquery(html)

        # Check title
        card_title = dom.find(".card__title")
        assert len(card_title) == 1
        assert card_title[0].text == card.title

        # Check image
        card_media = dom.find(".card__media")
        assert len(card_media) == 1

        card_image_url = card_media[0].cssselect("img")[0].get("src")
        assert card_image_url.startswith("/media/cache/") is True

        # Ensure there is no hidden sorl errors
        for log in self._caplog.record_tuples:
            if log[0].startswith("sorl.thumbnail.base") and log[1] == logging.ERROR:
                raise AssertionError("There is some 'sorl.thumbnail' error(s)")

        # Check content
        card_content = dom.find(".card__content p")
        assert len(card_content) == 1
        assert card_content[0].text == "Lorem ipsum dolore"

    def test_no_image(self):
        """
        When card has no image, image part should not be rendered
        """
        card = CardFactory(image=None)

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            image=card.image,
            content=card.content,
        )

        dom = html_pyquery(html)

        # Check image
        card_media = dom.find(".card__media")
        assert len(card_media) == 0

        # Check content
        card_content = dom.find(".card__content")
        assert len(card_content) == 1
        assert card_content[0].text == card.content

    def test_no_content(self):
        """
        When card has no content, content part should not be rendered
        """
        card = CardFactory(content="")

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            image=card.image,
            content=card.content,
        )

        dom = html_pyquery(html)

        card_content = dom.find(".card__content")
        assert len(card_content) == 0

    def test_feature_classes(self):
        """
        When card has features, their classes should be in .card 'class' attribute
        without duplicates.
        """
        card = CardFactory(
            features=["foo", "blob", "foo"]
        )

        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            image=card.image,
            content=card.content,
            features=card.features,
        )

        dom = html_pyquery(html)

        assert ["foo", "blob"] == [
            item
            for item in dom.attr("class").split()
            if item != "card"
        ]

    def test_link(self):
        """
        Depending card has a link or not, its wrapper tag should be respectively a
        '<a>' or a '<div>'.
        """
        card = CardFactory(image=None)

        # Without link
        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            features=card.features,
        )
        dom = html_pyquery(html)
        assert html.strip().startswith("<div") is True
        assert html.strip().endswith("</div>") is True

        # With a link
        placeholder, model_instance, context, html = self.create_basic_render(
            CardPlugin,
            template=card.template,
            features=card.features,
            link_url=card.link_url,
            link_open_blank=True,
        )
        dom = html_pyquery(html)
        assert html.strip().startswith("<a") is True
        assert html.strip().endswith("</a>") is True
        wrapper = dom.eq(0)
        assert wrapper.attr("href") == card.link_url
        assert wrapper.attr("target") == "_blank"

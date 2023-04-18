from django.conf import settings
from django.test import override_settings

from cms.api import create_page, add_plugin
from cms.utils.urlutils import admin_reverse

from cmsplugin_blocks.cms_plugins import CardPlugin
from cmsplugin_blocks.factories import CardFactory, UserFactory

from cmsplugin_blocks.utils.cms_tests import CMSPluginTestCase
from cmsplugin_blocks.utils.tests import html_pyquery

from tests.utils import FixturesTestCaseMixin


class CardCMSPluginsTestCase(FixturesTestCaseMixin, CMSPluginTestCase):
    """
    Card plugin tests case
    """

    def test_form_view_add(self):
        """
        Plugin creation form should return a success status code and every
        expected field should be present in HTML.
        """
        self.client.force_login(
            UserFactory(is_staff=True, is_superuser=True)
        )

        # Create dummy page
        page = create_page(
            language="en",
            title="Dummy",
            slug="dummy",
            template=settings.TEST_PAGE_TEMPLATES,
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

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Parse resulting plugin fields
        dom = html_pyquery(response)

        title_field = dom.find("input#id_title")
        assert len(title_field) == 1

        template_field = dom.find("select#id_template")
        assert len(template_field) == 1

        image_field = dom.find("input#id_image")
        assert len(image_field) == 1

        content_field = dom.find("textarea#id_content")
        assert len(content_field) == 1

        features_field = dom.find("select#id_features")
        assert len(features_field) == 1

    @override_settings(BLOCKS_CARD_FEATURES=[])
    def test_form_view_empty_features(self):
        """
        Plugin should not display 'features' field when there is no feature choices
        available from settings.
        """
        self.client.force_login(
            UserFactory(is_staff=True, is_superuser=True)
        )

        # Create dummy page
        page = create_page(
            language="en",
            title="Dummy",
            slug="dummy",
            template=settings.TEST_PAGE_TEMPLATES,
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

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Parse resulting plugin fields
        dom = html_pyquery(response)

        # Feature field is hidden since there is no feature choices
        features_field = dom.find("select#id_features")
        assert len(features_field) == 0

        # Field in the same tuple is still there
        image_field = dom.find("input#id_image")
        assert len(image_field) == 1

    def test_form_view_edit(self):
        """
        Plugin edition form should return a success status code and every
        expected field should be present in HTML.
        """
        self.client.force_login(
            UserFactory(is_staff=True, is_superuser=True)
        )

        # Create random values for parameters with a factory
        card = CardFactory(content="<p>Lorem ipsum dolore</p>")

        # Create dummy page
        page = create_page(
            language="en",
            title="Dummy",
            slug="dummy",
            template=settings.TEST_PAGE_TEMPLATES,
        )

        # Add card plugin to placeholder
        placeholder = page.placeholders.get(slot="content")
        model_instance = add_plugin(
            placeholder,
            CardPlugin,
            "en",
            template=card.template,
            features=card.features,
            image=card.image,
            content=card.content,
        )

        # Get the edition plugin form url and open it
        url = admin_reverse('cms_page_edit_plugin', args=[model_instance.id])
        response = self.client.get(url)

        # Expected http success status
        self.assertEqual(response.status_code, 200)

        # Parse resulting plugin fields
        dom = html_pyquery(response)

        title_field = dom.find("input#id_title")
        assert len(title_field) == 1

        template_field = dom.find("select#id_template")
        assert len(template_field) == 1

        image_field = dom.find("input#id_image")
        assert len(image_field) == 1

        content_field = dom.find("textarea#id_content")
        assert len(content_field) == 1

        features_field = dom.find("select#id_features")
        assert len(features_field) == 1

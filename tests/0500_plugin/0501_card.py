from cms.api import create_page, add_plugin

from cmsplugin_blocks.cms_plugins import CardPlugin
from cmsplugin_blocks.compat.cms import CmsAPI
from cmsplugin_blocks.factories import CardFactory, UserFactory
from cmsplugin_blocks.utils.tests import html_pyquery


def test_form_view_add(db, client, settings):
    """
    Plugin creation form should return a success status code and every
    expected field should be present in HTML.
    """
    cmsapi = CmsAPI()
    client.force_login(UserFactory(is_staff=True, is_superuser=True))

    # Create dummy page
    page = create_page(
        language="en",
        title="Dummy",
        slug="dummy",
        template=settings.TEST_PAGE_TEMPLATES,
    )

    # Get placeholder
    placeholder = cmsapi.get_placeholders(page).get(slot="content")

    # Get the edition plugin form
    response = cmsapi.request_plugin_add(client, "CardPlugin", placeholder.pk)

    # Expected http success status
    assert response.status_code == 200

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

    size_features_field = dom.find("a#add_id_size_features")
    assert len(size_features_field) == 1

    color_features_field = dom.find("a#add_id_color_features")
    assert len(color_features_field) == 1

    extra_features_field = dom.find("a#add_id_extra_features")
    assert len(extra_features_field) == 1


def test_form_view_edit(db, client, settings):
    """
    Plugin edition form should return a success status code and every
    expected field should be present in HTML.
    """
    cmsapi = CmsAPI()
    client.force_login(UserFactory(is_staff=True, is_superuser=True))

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
    placeholder = cmsapi.get_placeholders(page).get(slot="content")
    model_instance = add_plugin(
        placeholder,
        CardPlugin,
        "en",
        template=card.template,
        image=card.image,
        content=card.content,
    )

    # Get the edition plugin form url
    response = cmsapi.request_plugin_edit(client, model_instance.id)

    # Expected http success status
    assert response.status_code == 200

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

    size_features_field = dom.find("a#add_id_size_features")
    assert len(size_features_field) == 1

    color_features_field = dom.find("a#add_id_color_features")
    assert len(color_features_field) == 1

    extra_features_field = dom.find("a#add_id_extra_features")
    assert len(extra_features_field) == 1

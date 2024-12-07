from cms.api import create_page, add_plugin
from cms.models import Placeholder

from cmsplugin_blocks.cms_plugins import SliderPlugin
from cmsplugin_blocks.compat.cms import CmsAPI
from cmsplugin_blocks.factories import SliderFactory, SlideItemFactory, UserFactory
from cmsplugin_blocks.utils.tests import html_pyquery


def test_queryset_items_order(db):
    """
    Item order should be respected
    """
    slider = SliderFactory()

    # Create item in various order
    SlideItemFactory.create(slider=slider, order=3, title="3")
    SlideItemFactory.create(slider=slider, order=1, title="1")
    SlideItemFactory.create(slider=slider, order=2, title="2")
    SlideItemFactory.create(slider=slider, order=4, title="4")

    # Build plugin
    placeholder = Placeholder.objects.create(slot="test")
    model_instance = add_plugin(
        placeholder,
        SliderPlugin,
        "en",
        template=slider.template,
        title=slider.title,
    )
    model_instance.copy_relations(slider)

    # Get the ressources queryset from plugin render context
    plugin_instance = model_instance.get_plugin_class_instance()
    context = plugin_instance.render({}, model_instance, None)
    items = [(item.title, item.order) for item in context["slides"]]

    assert items == [("1", 1), ("2", 2), ("3", 3), ("4", 4)]


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
    response = cmsapi.request_plugin_add(client, "SliderPlugin", placeholder.pk)

    # Expected http success status
    assert response.status_code == 200

    # Parse resulting plugin fields
    dom = html_pyquery(response)

    title_field = dom.find("input#id_title")
    assert len(title_field) == 1

    template_field = dom.find("select#id_template")
    assert len(template_field) == 1

    size_features_field = dom.find("a#add_id_size_features")
    assert len(size_features_field) == 1

    color_features_field = dom.find("a#add_id_color_features")
    assert len(color_features_field) == 1

    extra_features_field = dom.find("a#add_id_extra_features")
    assert len(extra_features_field) == 1

    # All template input to add new item
    item_content_field = dom.find("textarea#id_slide_item-__prefix__-content")
    assert len(item_content_field) == 1

    item_image_field = dom.find("input#id_slide_item-__prefix__-image")
    assert len(item_image_field) == 1

    item_order_field = dom.find("input#id_slide_item-__prefix__-order")
    assert len(item_order_field) == 1

    item_link_name_field = dom.find("input#id_slide_item-__prefix__-link_name")
    assert len(item_link_name_field) == 1

    item_link_url_field = dom.find("input#id_slide_item-__prefix__-link_url")
    assert len(item_link_url_field) == 1

    item_link_blank_field = dom.find(
        "input[type=checkbox]#id_slide_item-__prefix__-link_open_blank"
    )
    assert len(item_link_blank_field) == 1


def test_form_view_edit(db, client, settings):
    """
    Plugin edition form should return a success status code and every
    expected field should be present in HTML.
    """
    cmsapi = CmsAPI()
    client.force_login(UserFactory(is_staff=True, is_superuser=True))

    # Create random values for parameters with a factory
    slider = SliderFactory()
    SlideItemFactory.create(
        slider=slider,
    )

    # Create dummy page
    page = create_page(
        language="en",
        title="Dummy",
        slug="dummy",
        template=settings.TEST_PAGE_TEMPLATES,
    )

    # Add slider plugin to placeholder
    placeholder = cmsapi.get_placeholders(page).get(slot="content")
    model_instance = add_plugin(
        placeholder,
        SliderPlugin,
        "en",
        template=slider.template,
        title=slider.title,
    )
    model_instance.copy_relations(slider)

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

    size_features_field = dom.find("a#add_id_size_features")
    assert len(size_features_field) == 1

    color_features_field = dom.find("a#add_id_color_features")
    assert len(color_features_field) == 1

    extra_features_field = dom.find("a#add_id_extra_features")
    assert len(extra_features_field) == 1

    # Some template inputs to add new item
    item_content_field = dom.find("textarea#id_slide_item-__prefix__-content")
    assert len(item_content_field) == 1

    # Inputs for existing item
    item_content_field = dom.find("textarea#id_slide_item-0-content")
    assert len(item_content_field) == 1

    # There should be no more than a single item
    item_content_field = dom.find("textarea#id_slide_item-1-content")
    assert len(item_content_field) == 0

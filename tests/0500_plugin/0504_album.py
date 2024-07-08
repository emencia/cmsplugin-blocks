from cms.api import create_page, add_plugin
from cms.models import Placeholder
from cms.utils.urlutils import admin_reverse

from cmsplugin_blocks.cms_plugins import AlbumPlugin
from cmsplugin_blocks.factories import AlbumFactory, AlbumItemFactory, UserFactory
from cmsplugin_blocks.utils.tests import html_pyquery


def test_queryset_items_order(db, client, tests_settings, settings):
    """
    Item order should be respected
    """
    album = AlbumFactory()

    # Create item in various order
    AlbumItemFactory.create(album=album, order=3, title="3")
    AlbumItemFactory.create(album=album, order=1, title="1")
    AlbumItemFactory.create(album=album, order=2, title="2")
    AlbumItemFactory.create(album=album, order=4, title="4")

    # Build plugin
    placeholder = Placeholder.objects.create(slot="test")
    model_instance = add_plugin(
        placeholder,
        AlbumPlugin,
        "en",
        template=album.template,
        title=album.title,
    )
    model_instance.copy_relations(album)

    # Get the ressources queryset from plugin render context
    plugin_instance = model_instance.get_plugin_class_instance()
    context = plugin_instance.render({}, model_instance, None)
    items = [(item.title, item.order) for item in context["ressources"]]

    assert items == [('1', 1), ('2', 2), ('3', 3), ('4', 4)]

def test_form_view_add(db, client, tests_settings, settings):
    """
    Plugin creation form should return a success status code and every
    expected field should be present in HTML.
    """
    client.force_login(UserFactory(is_staff=True, is_superuser=True))

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
    response = client.get(url, {
        'plugin_type': 'AlbumPlugin',
        'placeholder_id': placeholder.pk,
        'target_language': 'en',
        'plugin_language': 'en',
    })

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
    item_title_field = dom.find("input#id_album_item-__prefix__-title")
    assert len(item_title_field) == 1

    item_image_field = dom.find("input#id_album_item-__prefix__-image")
    assert len(item_image_field) == 1

    item_order_field = dom.find("input#id_album_item-__prefix__-order")
    assert len(item_order_field) == 1

    # There should not be existing item
    item_image_field = dom.find("input#id_album_item-0-image")
    assert len(item_image_field) == 0

    item_order_field = dom.find("input#id_album_item-0-order")
    assert len(item_order_field) == 0

def test_form_view_edit(db, client, tests_settings, settings):
    """
    Plugin edition form should return a success status code and every
    expected field should be present in HTML.
    """
    client.force_login(UserFactory(is_staff=True, is_superuser=True))

    # Create random values for parameters with a factory
    album = AlbumFactory()
    AlbumItemFactory.create(
        album=album,
    )

    # Create dummy page
    page = create_page(
        language="en",
        title="Dummy",
        slug="dummy",
        template=settings.TEST_PAGE_TEMPLATES,
    )

    # Add album plugin to placeholder
    placeholder = page.placeholders.get(slot="content")
    model_instance = add_plugin(
        placeholder,
        AlbumPlugin,
        "en",
        template=album.template,
        title=album.title,
    )
    model_instance.copy_relations(album)

    # Get the edition plugin form url and open it
    url = admin_reverse('cms_page_edit_plugin', args=[model_instance.id])
    response = client.get(url)

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

    # Some template input to add new item
    item_title_field = dom.find("input#id_album_item-__prefix__-title")
    assert len(item_title_field) == 1

    # Inputs for existing item
    item_title_field = dom.find("input#id_album_item-0-title")
    assert len(item_title_field) == 1

    # There should be no more than a single item
    item_title_field = dom.find("input#id_album_item-1-title")
    assert len(item_title_field) == 0

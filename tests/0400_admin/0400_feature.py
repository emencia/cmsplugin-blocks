from django.urls import reverse

from cmsplugin_blocks.factories import FeatureFactory


def test_export_permission(db, client):
    """
    Exporting view should only be reachable for admins with 'is_staff' status.
    """
    url = reverse("admin:cmsplugin_blocks_feature_export")
    login_url = "{}?next={}".format(reverse("admin:login"), url)

    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain == [
        (login_url, 302)
    ]


def test_export_empty(db, admin_client):
    """
    Exporting view should work without any error when there is no feature yet.
    """
    url = reverse("admin:cmsplugin_blocks_feature_export")
    response = admin_client.get(url)
    assert response.status_code == 200

    payload = response.json()
    assert sorted(payload.keys()) == ["date", "items", "version"]
    assert len(payload["items"]) == 0


def test_export_content(db, admin_client, settings):
    """
    Exporting view should work without any error when there is some features.

    Also note how the exporter does not care about value syntax (Ping item contains
    whitespaces even it is not allowed from settings) because it is assumed that stored
    content has been well validated.
    """
    settings.BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES = False

    FeatureFactory(title="Foo", scope="size", plugins=["Card"])
    FeatureFactory(title="Bar", scope="size", plugins=["Album,Card"])
    FeatureFactory(title="Ping", value="ping floyd", scope="color", plugins=["Hero"])
    FeatureFactory(title="Pong", scope="extra", plugins=["Hero"])

    url = reverse("admin:cmsplugin_blocks_feature_export")
    response = admin_client.get(url)
    assert response.status_code == 200

    payload = response.json()
    assert payload["items"] == [
        {
            "title": "Ping",
            "value": "ping floyd",
            "scope": "color",
            "plugins": [
                "Hero"
            ]
        },
        {
            "title": "Pong",
            "value": "pong",
            "scope": "extra",
            "plugins": [
                "Hero"
            ]
        },
        {
            "title": "Bar",
            "value": "bar",
            "scope": "size",
            "plugins": [
                "Album",
                "Card"
            ]
        },
        {
            "title": "Foo",
            "value": "foo",
            "scope": "size",
            "plugins": [
                "Card"
            ]
        }
    ]

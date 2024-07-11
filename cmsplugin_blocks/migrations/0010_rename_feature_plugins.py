from django.db import migrations


def rename_plugins(apps, schema_editor):
    """
    Rename feature plugin names to match the new nomenclature.

    Unknow names will be forgotten.
    """
    historical_names = {
        "Album": "Album",
        "Card": "Card",
        "Hero": "Hero",
        "Container": "Container",
        "Slider": "Slider",
    }
    forgotten_names = ["AlbumItem", "SliderItem"]

    Feature = apps.get_model("cmsplugin_blocks", "Feature")
    for feature in Feature.objects.all():
        feature.plugins = [
            historical_names[name]
            for name in feature.plugins
            if name in historical_names
        ]
        feature.save()


class Migration(migrations.Migration):

    dependencies = [
        ("cmsplugin_blocks", "0009_refactoring_features_for_container_album_slider"),
    ]

    operations = [
        migrations.RunPython(rename_plugins),
    ]

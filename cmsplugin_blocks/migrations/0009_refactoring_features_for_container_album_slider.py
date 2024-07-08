# Generated by Django 5.0.6 on 2024-07-08 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_blocks', '0008_refactoring_features_for_card_hero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='features',
        ),
        migrations.RemoveField(
            model_name='albumitem',
            name='features',
        ),
        migrations.RemoveField(
            model_name='container',
            name='features',
        ),
        migrations.AddField(
            model_name='album',
            name='color_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'AlbumMain', 'scope': 'color'}, related_name='%(app_label)s_%(class)s_color_related', to='cmsplugin_blocks.feature', verbose_name='color features'),
        ),
        migrations.AddField(
            model_name='album',
            name='extra_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'AlbumMain', 'scope': 'extra'}, related_name='%(app_label)s_%(class)s_extra_related', to='cmsplugin_blocks.feature', verbose_name='extra features'),
        ),
        migrations.AddField(
            model_name='album',
            name='size_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'AlbumMain', 'scope': 'size'}, related_name='%(app_label)s_%(class)s_size_related', to='cmsplugin_blocks.feature', verbose_name='size features'),
        ),
        migrations.AddField(
            model_name='container',
            name='color_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'ContainerMain', 'scope': 'color'}, related_name='%(app_label)s_%(class)s_color_related', to='cmsplugin_blocks.feature', verbose_name='color features'),
        ),
        migrations.AddField(
            model_name='container',
            name='extra_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'ContainerMain', 'scope': 'extra'}, related_name='%(app_label)s_%(class)s_extra_related', to='cmsplugin_blocks.feature', verbose_name='extra features'),
        ),
        migrations.AddField(
            model_name='container',
            name='size_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'ContainerMain', 'scope': 'size'}, related_name='%(app_label)s_%(class)s_size_related', to='cmsplugin_blocks.feature', verbose_name='size features'),
        ),
    ]

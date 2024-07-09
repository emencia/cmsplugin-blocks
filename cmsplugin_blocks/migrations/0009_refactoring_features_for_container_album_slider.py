# Generated by Django 5.0.6 on 2024-07-09 00:12

import cmsplugin_blocks.modelfields
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
        migrations.RemoveField(
            model_name='slideitem',
            name='features',
        ),
        migrations.RemoveField(
            model_name='slider',
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
        migrations.AddField(
            model_name='slider',
            name='color_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'SliderMain', 'scope': 'color'}, related_name='%(app_label)s_%(class)s_color_related', to='cmsplugin_blocks.feature', verbose_name='color features'),
        ),
        migrations.AddField(
            model_name='slider',
            name='extra_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'SliderMain', 'scope': 'extra'}, related_name='%(app_label)s_%(class)s_extra_related', to='cmsplugin_blocks.feature', verbose_name='extra features'),
        ),
        migrations.AddField(
            model_name='slider',
            name='size_features',
            field=models.ManyToManyField(blank=True, limit_choices_to={'plugins__contains': 'SliderMain', 'scope': 'size'}, related_name='%(app_label)s_%(class)s_size_related', to='cmsplugin_blocks.feature', verbose_name='size features'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='plugins',
            field=cmsplugin_blocks.modelfields.CommaSeparatedStringsField(blank=True, choices=[('AlbumMain', 'Album'), ('CardMain', 'Card'), ('HeroMain', 'Hero'), ('ContainerMain', 'Container'), ('SliderMain', 'Slider')], default='', max_length=50, verbose_name='Allowed for plugins'),
        ),
    ]
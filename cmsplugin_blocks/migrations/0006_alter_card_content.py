# Generated by Django 4.2.2 on 2023-07-03 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_blocks', '0005_v1-0-0_changes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='content',
            field=models.TextField(blank=True, default='', verbose_name='Content'),
        ),
    ]

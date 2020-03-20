# Generated by Django 2.1.9 on 2020-03-20 00:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_blocks', '0003_slideitem_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumitem',
            name='image',
            field=models.FileField(default=None, max_length=255, null=True, upload_to='blocks/album/%y/%m', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'svg', 'gif', 'png'])], verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.FileField(blank=True, default=None, max_length=255, null=True, upload_to='blocks/card/%y/%m', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'svg', 'gif', 'png'])], verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='image',
            field=models.FileField(blank=True, default=None, max_length=255, null=True, upload_to='blocks/hero/%y/%m', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'svg', 'gif', 'png'])], verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='slideitem',
            name='image',
            field=models.FileField(default=None, max_length=255, null=True, upload_to='blocks/slider/%y/%m', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'svg', 'gif', 'png'])], verbose_name='Image'),
        ),
    ]

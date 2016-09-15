# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocker', '0013_auto_20160914_1603'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mocker',
            old_name='content_type',
            new_name='destination_content_type',
        ),
        migrations.AddField(
            model_name='mocker',
            name='return_content_type',
            field=models.CharField(choices=[('application/json', 'application/json'), ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'), ('application/xhtml+xml', 'application/xhtml+xml'), ('multipart/form-data', 'multipart/form-data'), ('text/css', 'text/css'), ('text/csv', 'text/csv'), ('text/html', 'text/html'), ('text/json', 'text/json'), ('text/plain', 'text/plain'), ('text/xml', 'text/xml')], default=1, max_length=256, verbose_name='Callback return content type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mocker',
            name='short_id',
            field=models.CharField(max_length=256, verbose_name='Short ID'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-24 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mocker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updation_date', models.DateTimeField(auto_now=True, verbose_name='Updation date')),
                ('original_destination_address', models.URLField(verbose_name='Destination API address to be mocked')),
                ('callback_address', models.URLField(blank=True, null=True, verbose_name='Callback API address')),
                ('callback_content_type', models.CharField(blank=True, choices=[('application/json', 'application/json')], max_length=256, null=True, verbose_name='Callback API content type')),
                ('hashed_id', models.CharField(max_length=128, verbose_name='Hashed ID')),
                ('mocked_address', models.URLField(blank=True, null=True, verbose_name='Mocked API Address')),
                ('mocked_allowed_http_method', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET'), ('PATCH', 'PATCH'), ('PUT', 'PUT')], max_length=256, verbose_name='Allowed HTTP method for a mocked API')),
                ('mocked_allowed_content_type', models.CharField(choices=[('application/json', 'application/json')], max_length=256, verbose_name='Allowed content type for a mocked API')),
            ],
            options={
                'verbose_name': 'Mocked API',
                'verbose_name_plural': 'Mocked APIs',
            },
        ),
    ]

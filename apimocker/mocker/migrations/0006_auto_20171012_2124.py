# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mocker', '0005_auto_20171012_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mocker',
            name='custom_header',
        ),
        migrations.AddField(
            model_name='customheader',
            name='mocker',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='mocker.Mocker', verbose_name='Mocker'),
            preserve_default=False,
        ),
    ]

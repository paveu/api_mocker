# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mocker', '0006_auto_20171012_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responselog',
            name='mocker',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='mocker.Mocker', verbose_name='Mocker'),
            preserve_default=False,
        ),
    ]
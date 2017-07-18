# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 18:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mocker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('destination_address', models.URLField(null=True, verbose_name='Called API')),
                ('content', models.TextField(null=True, verbose_name='API Response')),
            ],
            options={
                'verbose_name': 'API Log',
                'verbose_name_plural': 'API Logs',
            },
        ),
        migrations.RemoveField(
            model_name='mocker',
            name='api_log',
        ),
        migrations.DeleteModel(
            name='APILog',
        ),
        migrations.AddField(
            model_name='responsecontent',
            name='mocker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mocker.Mocker'),
        ),
    ]

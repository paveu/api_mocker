# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 15:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mocker', '0010_auto_20160914_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='HTTP_Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET'), ('PATCH', 'PATCH'), ('DELETE', 'DELETE')], max_length=128, verbose_name='HTTP method')),
            ],
        ),
        migrations.AlterField(
            model_name='mocker',
            name='http_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mocker.HTTP_Method', verbose_name='HTTP Method'),
        ),
        migrations.DeleteModel(
            name='HTTP_METHODS',
        ),
    ]

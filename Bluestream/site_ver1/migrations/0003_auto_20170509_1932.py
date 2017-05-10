# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_ver1', '0002_project_projectmembers'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone_number',
            field=models.CharField(default='000-000-0000', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.CharField(default='client', max_length=50),
            preserve_default=False,
        ),
    ]

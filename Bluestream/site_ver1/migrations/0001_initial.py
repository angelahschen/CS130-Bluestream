# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 05:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=70, primary_key=True, serialize=False)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-08 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import site_ver1.models


class Migration(migrations.Migration):

    dependencies = [
        ('site_ver1', '0002_auto_20170607_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsection8',
            name='certification',
            field=models.FileField(upload_to=site_ver1.models.get_cert_upload_filename, validators=[site_ver1.models.FileValidator(content_types='application/pdf')], verbose_name='Select a file'),
        ),
        migrations.AlterField(
            model_name='formsection8',
            name='disclosure',
            field=models.FileField(upload_to=site_ver1.models.get_disc_upload_filename, validators=[site_ver1.models.FileValidator(content_types='application/pdf')], verbose_name='Select a file'),
        ),
    ]

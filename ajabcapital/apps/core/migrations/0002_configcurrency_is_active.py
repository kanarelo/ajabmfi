# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configcurrency',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

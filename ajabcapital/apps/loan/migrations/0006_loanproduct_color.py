# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-26 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0005_auto_20160426_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanproduct',
            name='color',
            field=models.CharField(max_length=15, null=True),
        ),
    ]

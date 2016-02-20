# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 07:48
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0021_auto_20160219_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configloanriskclassification',
            name='default_provision',
            field=models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=7),
        ),
    ]
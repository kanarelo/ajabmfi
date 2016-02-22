# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 00:30
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0025_auto_20160221_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanproduct',
            name='default_amount',
            field=models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=18),
        ),
    ]
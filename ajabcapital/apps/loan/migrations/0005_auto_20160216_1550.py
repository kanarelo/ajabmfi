# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_auto_20160216_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanproduct',
            name='grace_period_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.ConfigGracePeriodType'),
        ),
    ]

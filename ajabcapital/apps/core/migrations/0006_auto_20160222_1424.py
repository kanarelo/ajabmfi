# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_configledgeraccountcategory_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledgeraccount',
            name='account_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.ConfigLedgerAccountCategory'),
        ),
    ]

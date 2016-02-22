# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('loan', '0027_remove_loanproduct_amount_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanproduct',
            name='amount_currency',
            field=models.ForeignKey(db_column='currency', default=1, on_delete=django.db.models.deletion.CASCADE, to='core.ConfigCurrency'),
            preserve_default=False,
        ),
    ]
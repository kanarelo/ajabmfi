# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0022_auto_20160219_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanaccounttransactionentry',
            name='ledger_type',
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='default_amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='default_installments',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='loantransaction',
            name='transaction_no',
            field=models.CharField(default=1, max_length=15, unique=True),
            preserve_default=False,
        ),
    ]
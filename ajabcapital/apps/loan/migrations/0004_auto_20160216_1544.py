# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 15:44
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_auto_20160216_1451'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loanaccountstatus',
            options={'verbose_name': 'Loan Account Status', 'verbose_name_plural': 'Loan Account Statuses'},
        ),
        migrations.AlterModelOptions(
            name='loanproductfundsource',
            options={'verbose_name': 'Loan Fund Source'},
        ),
        migrations.RenameField(
            model_name='loanproduct',
            old_name='sname',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='loanproductfee',
            name='transaction_type',
        ),
        migrations.AddField(
            model_name='loanproductfee',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=4),
        ),
        migrations.AddField(
            model_name='loanproductfee',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loan.ConfigCurrency'),
            preserve_default=False,
        ),
    ]

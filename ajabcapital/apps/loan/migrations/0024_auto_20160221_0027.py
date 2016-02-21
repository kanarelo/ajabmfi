# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 00:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('loan', '0023_auto_20160220_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanproduct',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='loanproduct',
            name='default_installments',
        ),
        migrations.RemoveField(
            model_name='loanproduct',
            name='max_installments',
        ),
        migrations.RemoveField(
            model_name='loanproduct',
            name='min_installments',
        ),
        migrations.RemoveField(
            model_name='loanproduct',
            name='period_unit',
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='amount_currency',
            field=models.ForeignKey(blank=True, db_column='currency', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ConfigCurrency'),
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='default_grace_period_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grace_products', to='loan.ConfigLoanPeriodUnit'),
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='default_installment',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='default_repayment_period_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='repayment_products', to='loan.ConfigLoanPeriodUnit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='max_installment',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='min_installment',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loanproduct',
            name='default_grace_period',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

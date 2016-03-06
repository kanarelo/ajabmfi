# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 07:18
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0049_auto_20160224_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanproductaccountingrule',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='loanproductaccountingrule',
            name='credit_account',
        ),
        migrations.RemoveField(
            model_name='loanproductaccountingrule',
            name='debit_account',
        ),
        migrations.RemoveField(
            model_name='loanproductaccountingrule',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='loanproductaccountingrule',
            name='product',
        ),
        migrations.RemoveField(
            model_name='loanproductaccountingrule',
            name='transaction_type',
        ),
        migrations.RemoveField(
            model_name='loanaccount',
            name='next_interest_accrual_date',
        ),
        migrations.AddField(
            model_name='loanaccount',
            name='last_accrual_amount',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.0'), max_digits=18),
        ),
        migrations.AddField(
            model_name='loanaccount',
            name='last_accrual_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='configloanperiodunit',
            name='frequencies',
            field=models.ManyToManyField(to='loan.ConfigRepaymentFrequency'),
        ),
        migrations.AlterField(
            model_name='loanaccount',
            name='repayment_frequency',
            field=models.ForeignKey(db_column='payment_frequency', on_delete=django.db.models.deletion.CASCADE, to='loan.ConfigRepaymentFrequency'),
        ),
        migrations.AlterField(
            model_name='loanproduct',
            name='default_repayment_frequency',
            field=models.ForeignKey(db_column='payment_frequency', default=1, on_delete=django.db.models.deletion.CASCADE, to='loan.ConfigRepaymentFrequency'),
        ),
        migrations.DeleteModel(
            name='LoanProductAccountingRule',
        ),
    ]
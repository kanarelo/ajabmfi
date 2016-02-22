# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 14:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160222_1433'),
        ('loan', '0038_auto_20160222_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanproductaccountingrule',
            name='credit_account',
            field=models.ForeignKey(default='1.1311.000', on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='core.LedgerAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanproductaccountingrule',
            name='debit_account',
            field=models.ForeignKey(default='1.1311.000', on_delete=django.db.models.deletion.CASCADE, related_name='debits', to='core.LedgerAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanproductcontrolaccount',
            name='base_account',
            field=models.ForeignKey(default='1.1311.000', on_delete=django.db.models.deletion.CASCADE, to='core.LedgerAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanproductfundsource',
            name='base_account',
            field=models.ForeignKey(default='1.1311.000', on_delete=django.db.models.deletion.CASCADE, to='core.LedgerAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loantransactionregister',
            name='loan_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loan.LoanAccount'),
            preserve_default=False,
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
    ]

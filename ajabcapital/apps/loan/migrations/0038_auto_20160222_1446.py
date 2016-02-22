# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 14:46
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_auto_20160222_1433'),
        ('loan', '0037_auto_20160222_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanTransactionRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='loan_loantransactionregister_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_loantransactionregister_deleted_by_me', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_register', to='core.LedgerTransaction')),
            ],
            options={
                'db_table': 'loan_transaction_register',
                'verbose_name': 'Loan Transaction Register',
            },
        ),
        migrations.RemoveField(
            model_name='configloanaccounttransactionstatus',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='configloanaccounttransactionstatus',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='configloantransactiontype',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='configloantransactiontype',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='loanaccounttransactionentry',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='loanaccounttransactionentry',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='loanaccounttransactionentry',
            name='loan_account',
        ),
        migrations.RemoveField(
            model_name='loanaccounttransactionentry',
            name='loan_ledger_account',
        ),
        migrations.RemoveField(
            model_name='loanaccounttransactionentry',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='loanledgeraccount',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='loanledgeraccount',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='loantransaction',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='loantransaction',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='loantransaction',
            name='status',
        ),
        migrations.RemoveField(
            model_name='loantransaction',
            name='transaction_type',
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
            model_name='loanproductcontrolaccount',
            name='base_account',
        ),
        migrations.RemoveField(
            model_name='loanproductcontrolaccount',
            name='rules',
        ),
        migrations.RemoveField(
            model_name='loanproductfundsource',
            name='base_account',
        ),
        migrations.AddField(
            model_name='loanproductcontrolaccount',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(default='{}'),
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
        migrations.AlterField(
            model_name='loanproductaccountingrule',
            name='transaction_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounting_rules', to='core.ConfigLedgerTransactionType'),
        ),
        migrations.AlterField(
            model_name='loanproductcontrolaccount',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='loan.LoanProduct'),
        ),
        migrations.DeleteModel(
            name='ConfigLoanAccountTransactionStatus',
        ),
        migrations.DeleteModel(
            name='ConfigLoanTransactionType',
        ),
        migrations.DeleteModel(
            name='LoanAccountTransactionEntry',
        ),
        migrations.DeleteModel(
            name='LoanLedgerAccount',
        ),
        migrations.DeleteModel(
            name='LoanTransaction',
        ),
    ]

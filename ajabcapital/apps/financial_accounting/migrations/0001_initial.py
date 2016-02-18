# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-18 16:27
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigGLAccountCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_configglaccountcategory_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_configglaccountcategory_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_gl_account_category',
                'verbose_name': 'Config General Ledegr Account Category',
                'verbose_name_plural': 'Config GL Account Categories',
            },
        ),
        migrations.CreateModel(
            name='ConfigGLAccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_configglaccounttype_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_configglaccounttype_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_gl_account_type',
                'verbose_name': 'Config GL Account Type',
            },
        ),
        migrations.CreateModel(
            name='ConfigGLTransactionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('icon', models.FileField(blank=True, null=True, upload_to='config/icons/')),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_configgltransactionstatus_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_configgltransactionstatus_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_gl_transaction_status',
                'verbose_name': 'Config GL Transaction Status',
                'verbose_name_plural': 'Config GL Transaction Statuses',
            },
        ),
        migrations.CreateModel(
            name='GeneralLedgerAccount',
            fields=[
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('gl_code', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('account_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_accounting.ConfigGLAccountCategory')),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_accounting.ConfigGLAccountType')),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_generalledgeraccount_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_generalledgeraccount_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'general_ledger_account',
                'verbose_name': 'General Ledger Account',
            },
        ),
        migrations.CreateModel(
            name='GeneralLedgerTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=4, default=Decimal('0.0'), max_digits=18)),
                ('notes', models.CharField(max_length=160, null=True)),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_generalledgertransaction_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ConfigCurrency')),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_generalledgertransaction_deleted_by_me', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_accounting.ConfigGLTransactionStatus')),
            ],
            options={
                'db_table': 'general_ledger_transaction',
                'verbose_name': 'General Ledger Transaction',
            },
        ),
        migrations.CreateModel(
            name='GeneralLedgerTransactionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_type', models.PositiveIntegerField(choices=[(0, 'Credit'), (1, 'Debit')])),
                ('gl_code', models.CharField(max_length=25, null=True)),
                ('ledger_balance_increment', models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=18)),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_generalledgertransactionentry_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financial_accounting_generalledgertransactionentry_deleted_by_me', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_accounting.GeneralLedgerTransaction')),
            ],
            options={
                'db_table': 'general_ledger_transaction_entry',
                'verbose_name': 'General Ledger Transaction Entries',
            },
        ),
    ]

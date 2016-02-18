# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 08:20
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan', '0009_auto_20160216_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigLoanPipelineStep',
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
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='loan_configloanpipelinestep_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_configloanpipelinestep_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_loan_pipeline_step',
                'verbose_name': 'Config Loan Pipeline Step',
            },
        ),
        migrations.CreateModel(
            name='LoanGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='loan_loangroup_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_loangroup_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'loan_group',
                'verbose_name': 'Loan Group',
            },
        ),
        migrations.CreateModel(
            name='LoanProductControlAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('rules', models.CharField(max_length=1000)),
                ('base_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.LoanLedgerAccount')),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='loan_loanproductcontrolaccount_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_loanproductcontrolaccount_deleted_by_me', to=settings.AUTH_USER_MODEL)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='control_account', to='loan.LoanProduct')),
            ],
            options={
                'db_table': 'loan_product_control_account',
                'verbose_name': 'Loan Fund Source',
            },
        ),
        migrations.CreateModel(
            name='LoanProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('no_of_loans', models.PositiveIntegerField()),
                ('no_of_current_loans', models.PositiveIntegerField()),
                ('no_of_closed_loans', models.PositiveIntegerField()),
                ('no_of_requests', models.PositiveIntegerField()),
                ('is_performing', models.BooleanField()),
                ('has_current_delinquency', models.BooleanField()),
                ('has_historical_delinquency', models.BooleanField()),
                ('min_days_in_arrears', models.PositiveIntegerField()),
                ('max_days_in_arrears', models.PositiveIntegerField()),
                ('first_disbursal', models.DateTimeField()),
                ('last_repayment', models.DateTimeField()),
                ('credit_limit', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=18)),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='loan_loanprofile_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_loanprofile_deleted_by_me', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_accounts', related_query_name='loan_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'loan_profile',
                'verbose_name': 'Loan Profile',
            },
        ),
        migrations.CreateModel(
            name='LoanProfileGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(db_column=b'created_by', on_delete=django.db.models.deletion.CASCADE, related_name='loan_loanprofilegroup_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column=b'deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_loanprofilegroup_deleted_by_me', to=settings.AUTH_USER_MODEL)),
                ('loan_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.LoanGroup')),
                ('loan_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.LoanProfile')),
            ],
            options={
                'db_table': 'loan_profile_group',
                'verbose_name': 'Loan Profile Group',
            },
        ),
        migrations.RenameField(
            model_name='loanaccount',
            old_name='credit_amortization_type',
            new_name='amortization_type',
        ),
        migrations.RemoveField(
            model_name='loanaccount',
            name='credit_limit',
        ),
        migrations.RemoveField(
            model_name='loanaccount',
            name='group_identification_number',
        ),
        migrations.RemoveField(
            model_name='loanaccount',
            name='holder',
        ),
        migrations.RemoveField(
            model_name='loanaccount',
            name='repayment_frequency',
        ),
        migrations.AddField(
            model_name='loanaccount',
            name='loan_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.LoanProfile'),
        ),
        migrations.AddField(
            model_name='loanaccount',
            name='loan_profile_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.LoanProfileGroup'),
        ),
    ]
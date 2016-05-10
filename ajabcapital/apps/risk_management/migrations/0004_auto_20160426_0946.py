# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-26 09:46
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('risk_management', '0003_auto_20160426_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigLoanRiskClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=15, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('system_defined', models.BooleanField(default=False)),
                ('default_provision', models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=7)),
                ('icon', models.FileField(blank=True, null=True, upload_to='config/icons/')),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='risk_management_configloanriskclassification_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='risk_management_configloanriskclassification_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_loan_risk_classification',
                'verbose_name': 'Config Loan Risk Classification',
            },
        ),
    ]
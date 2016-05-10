# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-26 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_auto_20160426_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanaccount',
            name='current_risk_classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classified_loan_accounts', related_query_name='classified_loan_account', to='risk_management.ConfigLoanRiskClassification'),
        ),
    ]
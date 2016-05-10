# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-26 09:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk_management', '0002_auto_20160426_0929'),
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configloanriskclassification',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='configloanriskclassification',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='loanriskclassification',
            name='account',
        ),
        migrations.RemoveField(
            model_name='loanriskclassification',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='loanriskclassification',
            name='classification',
        ),
        migrations.RemoveField(
            model_name='loanriskclassification',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='loanriskclassification',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='loanaccount',
            name='current_risk_classification',
        ),
        migrations.RemoveField(
            model_name='loanaccount',
            name='current_risk_classification_date',
        ),
        migrations.DeleteModel(
            name='LoanRiskClassification',
        ),
    ]
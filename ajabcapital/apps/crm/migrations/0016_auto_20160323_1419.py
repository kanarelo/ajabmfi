# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 14:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_auto_20160323_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configloangroupstatus',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='configloangroupstatus',
            name='deleted_by',
        ),
        migrations.AlterModelOptions(
            name='configloangrouptype',
            options={'verbose_name': 'Config Loan Group Type'},
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='last_group_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ConfigGroupProfileStatus'),
        ),
        migrations.DeleteModel(
            name='ConfigLoanGroupStatus',
        ),
    ]

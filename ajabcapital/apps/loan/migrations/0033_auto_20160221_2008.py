# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0032_auto_20160221_2006'),
    ]

    operations = [
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

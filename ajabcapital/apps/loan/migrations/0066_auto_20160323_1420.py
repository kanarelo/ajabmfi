# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0065_auto_20160323_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configloanperiodunit',
            name='frequencies',
            field=models.ManyToManyField(to='loan.ConfigRepaymentFrequency'),
        ),
        migrations.AlterField(
            model_name='loanproduct',
            name='default_repayment_frequency',
            field=models.ForeignKey(db_column='payment_frequency', default=1, on_delete=django.db.models.deletion.CASCADE, to='loan.ConfigRepaymentFrequency'),
        ),
        migrations.AlterField(
            model_name='loanterm',
            name='repayment_frequency',
            field=models.ForeignKey(db_column='payment_frequency', on_delete=django.db.models.deletion.CASCADE, to='loan.ConfigRepaymentFrequency'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 21:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0008_auto_20160216_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanproductfee',
            old_name='flat_fee_amount',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='loanproductfee',
            old_name='flat_fee_currency',
            new_name='currency',
        ),
        migrations.RemoveField(
            model_name='loanproductfee',
            name='percentage_amount',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_auto_20160323_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessprofile',
            name='first_disbursal_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='last_disbursal_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='first_disbursal_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='last_disbursal_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='individualprofile',
            name='first_disbursal_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='individualprofile',
            name='last_disbursal_date',
            field=models.DateTimeField(null=True),
        ),
    ]

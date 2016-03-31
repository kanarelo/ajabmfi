# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 19:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0007_auto_20160307_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'campaign',
            },
        ),
        migrations.CreateModel(
            name='ConfigCampaignSchedule',
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
                ('is_active', models.BooleanField(default=True)),
                ('system_defined', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='crm_configcampaignschedule_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crm_configcampaignschedule_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_campaign_schedule',
                'verbose_name': 'Config Campaign Schedule',
            },
        ),
        migrations.CreateModel(
            name='ConfigCampaignTrigger',
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
                ('is_active', models.BooleanField(default=True)),
                ('system_defined', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='crm_configcampaigntrigger_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crm_configcampaigntrigger_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_campaign_trigger',
                'verbose_name': 'Config Campaign Trigger',
            },
        ),
        migrations.CreateModel(
            name='ConfigCampaignType',
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
                ('is_active', models.BooleanField(default=True)),
                ('system_defined', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='crm_configcampaigntype_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crm_configcampaigntype_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_campaign_type',
                'verbose_name': 'Config Campaign Type',
            },
        ),
        migrations.CreateModel(
            name='ConfigSegmentType',
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
                ('is_active', models.BooleanField(default=True)),
                ('system_defined', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='crm_configsegmenttype_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crm_configsegmenttype_deleted_by_me', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'config_segment_type',
                'verbose_name': 'Config Segment Type',
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_comment', models.CharField(blank=True, max_length=250, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('reason_deleted', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='crm_segment_created_by_me', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crm_segment_deleted_by_me', to=settings.AUTH_USER_MODEL)),
                ('segment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ConfigSegmentType')),
            ],
            options={
                'db_table': 'segment',
            },
        ),
        migrations.RemoveField(
            model_name='confignotificationschedule',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='confignotificationschedule',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='confignotificationtrigger',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='confignotificationtrigger',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='notificationtemplate',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='notificationtemplate',
            name='trigger',
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='ConfigNotificationSchedule',
        ),
        migrations.DeleteModel(
            name='ConfigNotificationTrigger',
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ConfigCampaignType'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='created_by',
            field=models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='crm_campaign_created_by_me', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='deleted_by',
            field=models.ForeignKey(blank=True, db_column='deleted_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crm_campaign_deleted_by_me', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ConfigCampaignSchedule'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='trigger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ConfigCampaignTrigger'),
        ),
    ]

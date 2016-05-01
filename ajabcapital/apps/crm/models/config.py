from __future__ import unicode_literals

from django.db import models

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class ConfigProfileStatus(ConfigBase):
    class Meta:
        db_table = "config_profile_status"
        verbose_name = "Config Profile Status"
        ordering = ["code"]

class ConfigBusinessRole(ConfigBase):
    class Meta:
        db_table = "config_business_role"
        verbose_name = "Config Business Role"
        ordering = ["code"]

class ConfigDocumentType(ConfigBase):
    class Meta:
        db_table = "config_document_type"
        verbose_name = "Config Document Type"
        ordering = ["code"]

class ConfigCampaignTrigger(ConfigBase):
    class Meta:
        db_table = "config_campaign_trigger"
        verbose_name = "Config Campaign Trigger"
        ordering = ["code"]

class ConfigIdentityType(ConfigBase):
    class Meta:
        db_table = "config_identity_type"
        verbose_name = "Config Identity Type"
        ordering = ["code"]

class ConfigMessageType(ConfigBase):
    class Meta:
        db_table = "config_message_type"
        verbose_name = "Config Message Type"  
        ordering = ["code"]

class ConfigMessageStatus(ConfigBase):
    class Meta:
        db_table = "config_message_status"
        verbose_name = "Config Message Status"
        verbose_name_plural = "Config Message Statuses"
        ordering = ["code"]

class ConfigCampaignType(ConfigBase):
    class Meta:
        db_table = "config_campaign_type"
        verbose_name = "Config Campaign Type"
        ordering = ["code"]

class ConfigCampaignSegmentType(ConfigBase):
    class Meta:
        db_table = "config_campaign_segment_type"
        verbose_name = "Config Campaign Segment Type"
        ordering = ["code"]

class ConfigLoanGroupRole(ConfigBase):
    class Meta:
        db_table = "config_loan_group_role"
        verbose_name = "Config Loan Group Role"
        ordering = ["code"]

class ConfigLoanGroupType(ConfigBase):
    class Meta:
        db_table = "config_loan_group_type"
        verbose_name = "Config Loan Group Type"
        ordering = ["code"]

class ConfigBusinessType(ConfigBase):
    class Meta:
        db_table = "config_business_type"
        verbose_name = "Config Business Type"
        verbose_name_plural = "Config Business Type"
        ordering = ["code"]

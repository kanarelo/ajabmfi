from __future__ import unicode_literals

from django.db import models

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class ConfigBusinessProfileStatus(ConfigBase):
    class Meta:
        db_table = "config_business_profile_status"
        verbose_name = "Config Business Profile Status"

class ConfigBusinessRole(ConfigBase):
    class Meta:
        db_table = "config_business_role"
        verbose_name = "Config Business Role"

class ConfigDocumentType(ConfigBase):
    class Meta:
        db_table = "config_document_type"
        verbose_name = "Config Document Type"

class ConfigCampaignTrigger(ConfigBase):
    class Meta:
        db_table = "config_campaign_trigger"
        verbose_name = "Config Campaign Trigger"

class ConfigCampaignSchedule(ConfigBase):
    class Meta:
        db_table = "config_campaign_schedule"
        verbose_name = "Config Campaign Schedule"

class ConfigIdentityType(ConfigBase):
    class Meta:
        db_table = "config_identity_type"
        verbose_name = "Config Identity Type"

class ConfigMessageType(ConfigBase):
    class Meta:
        db_table = "config_message_type"
        verbose_name = "Config Message Type"    

class ConfigMessageAction(ConfigBase):
    class Meta:
        db_table = "config_message_action"
        verbose_name = "Config Message Action"

class ConfigMessageStatus(ConfigBase):
    class Meta:
        db_table = "config_message_status"
        verbose_name = "Config Message Status"
        verbose_name_plural = "Config Message Statuses"

class ConfigCampaignType(ConfigBase):
    class Meta:
        db_table = "config_campaign_type"
        verbose_name = "Config Campaign Type"

class ConfigCampaignSegmentType(ConfigBase):
    class Meta:
        db_table = "config_campaign_segment_type"
        verbose_name = "Config Campaign Segment Type"

class ConfigGroupProfileStatus(ConfigBase):
    class Meta:
        db_table = "config_group_profile_status"
        verbose_name = "Config Group Profile Status"

class ConfigLoanGroupRole(ConfigBase):
    class Meta:
        db_table = "config_loan_group_role"
        verbose_name = "Config Loan Group Role"

class ConfigLoanGroupType(ConfigBase):
    class Meta:
        db_table = "config_loan_group_type"
        verbose_name = "Config Loan Group Type"

class ConfigBusinessType(ConfigBase):
    class Meta:
        db_table = "config_business_type"
        verbose_name = "Config Business Type"
        verbose_name_plural = "Config Business Type"

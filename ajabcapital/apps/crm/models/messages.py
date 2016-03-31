from __future__ import unicode_literals

from django.db import models

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class MessageTemplate(AuditBase):
    name = models.CharField(max_length=50)

    action = models.ForeignKey('ConfigMessageAction')
    template = models.CharField(max_length=500)

    class Meta:
        db_table = "message_template"
        verbose_name = "Message Template"

class Message(AuditBase):
    message_type = models.ForeignKey('ConfigMessageType')

    template = models.ForeignKey('MessageTemplate', null=True)
    
    individual_profile = models.ForeignKey('IndividualProfile', null=True, related_name="individual_messages")
    business_profile = models.ForeignKey('BusinessProfile', null=True, related_name="business_messages")
    group_profile = models.ForeignKey('GroupProfile', null=True, related_name="group_messages")

    message = models.CharField(max_length=800)

    status = models.ForeignKey('ConfigMessageStatus')

    class Meta:
        db_table = "message"

class CampaignSegment(ConfigBase):
    campaign_segment_type = models.ForeignKey('ConfigCampaignSegmentType')

    class Meta:
        db_table = "segment"

class Campaign(AuditBase):
    name = models.CharField(max_length=100)
    segment = models.ForeignKey('CampaignSegment')

    campaign_type = models.ForeignKey('ConfigCampaignType')

    #if it doesnt have a trigger, then we can do a batch
    trigger = models.ForeignKey('ConfigCampaignTrigger', null=True)
    schedule = models.ForeignKey('ConfigCampaignSchedule', null=True)

    class Meta:
        db_table = "campaign"

from __future__ import unicode_literals

from django.db import models

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class CampaignSegment(ConfigBase):
    campaign_segment_type = models.ForeignKey('ConfigCampaignSegmentType')

    class Meta:
        db_table = "segment"
        ordering = ["code"]

class Campaign(ConfigBase):
    campaign_type = models.ForeignKey('ConfigCampaignType')

    trigger  = models.ForeignKey('ConfigCampaignTrigger', null=True, blank=True)
    segment = models.ForeignKey('CampaignSegment', null=True, blank=True)
    template = models.ForeignKey('MessageTemplate', null=True, blank=True)

    message = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "campaign"

    def __str__(self):
        return self.name

class MessageTemplate(ConfigBase):
    template = models.CharField(max_length=500)

    class Meta:
        db_table = "message_template"
        verbose_name = "Message Template"

class Message(AuditBase):
    message_type = models.ForeignKey('ConfigMessageType')

    template = models.ForeignKey('MessageTemplate', null=True)
    campaign = models.ForeignKey('Campaign', null=True, related_name="messages")
    
    individual_profile = models.ForeignKey('IndividualProfile', 
        null=True, blank=True, related_name="individual_messages"
    )
    business_profile = models.ForeignKey('BusinessProfile', 
        null=True,  blank=True, related_name="business_messages"
    )
    group_profile = models.ForeignKey('GroupProfile', 
        null=True, blank=True, related_name="group_messages"
    )

    message = models.CharField(max_length=800)
    status = models.ForeignKey('ConfigMessageStatus')

    class Meta:
        db_table = "message"

    def __str__(self):
        return "%s for %s" % (self.message, (
            self.individual_profile or
            self.business_profile or
            self.group_profile
        ))

    def profile(self):
        return (
            self.individual_profile or
            self.business_profile or
            self.group_profile
        )

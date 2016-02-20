from __future__ import unicode_literals

from django.db import models

from ajabcapital.apps.core.models import (
    AuditBase, ConfigBase
)

class CustomerProfile(AuditBase):
    user = models.OneToOneField('core_users.User', null=True, blank=True)
    
    #if the user is blank: not all users can log into the portal
    mobile_phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    is_active = models.BooleanField(default=False)

    @property
    def whatsapp_user_id(self):
        return "254%s" % self.mobile_phone_number[1:]

    class Meta:
        db_table = "crm_customer_profile"
        verbose_name = "Customer Profile"

class ConfigNotificationAction(ConfigBase):
    class Meta:
        db_table = "config_notification_action"
        verbose_name = "Config Notification Action"

class ConfigNotificationTrigger(ConfigBase):
    class Meta:
        db_table = "config_notification_trigger"
        verbose_name = "Config Notification Trigger"

class ConfigNotificationStatus(ConfigBase):
    class Meta:
        db_table = "config_notification_status"
        verbose_name = "Config Notification Status"
        verbose_name_plural = "Config Notification Statuses"

class ConfigNotificationSchedule(ConfigBase):
    class Meta:
        db_table = "config_notification_schedule"
        verbose_name = "Config Notification Schedule"

class ConfigNotificationType(ConfigBase):
    class Meta:
        db_table = "config_notification_type"
        verbose_name = "Config Notification Type"    

class NotificationTemplate(AuditBase):
    name = models.CharField(max_length=50)

    #if it doesnt have a trigger, then we can do a batch
    trigger = models.ForeignKey('ConfigNotificationTrigger', null=True)
    schedule = models.ForeignKey('ConfigNotificationSchedule', null=True)

    action = models.ForeignKey('ConfigNotificationAction')

    template = models.CharField(max_length=500)

    class Meta:
        db_table = "notification_template"
        verbose_name = "Notification Template"

class Notification(AuditBase):
    notification_type = models.ForeignKey('ConfigNotificationType')

    template = models.ForeignKey('NotificationTemplate', null=True)
    profile = models.ForeignKey('CustomerProfile')

    message = models.CharField(max_length=800)

    status = models.ForeignKey('ConfigNotificationStatus')

    class Meta:
        db_table = "notification"

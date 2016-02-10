from django.conf import settings
from django.db import models

class AuditBase(models.Model):
    row_comment = models.CharField(max_length=250, null=True, blank=True)

    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_deleted_by_me",
        null=True, blank=True, db_column="deleted_by"
    )

    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)
    reason_deleted = models.CharField(max_length=250, null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_created_by_me",
        null=False, db_column="created_by"
    )
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ConfigBase(AuditBase):
    '''Class Account Closure Reason'''
    config_code = models.CharField(max_length=10)
    config_name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.config_name

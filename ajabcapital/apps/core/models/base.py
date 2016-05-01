from __future__ import unicode_literals

from django.conf import settings

from django.db import models
from django.db.models import Q, Sum, F

from decimal import Decimal as D

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ConfigBase(AuditBase):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, unique=True)

    is_active = models.BooleanField(default=True)
    system_defined = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

#---------------------------------------------------------------
# Balances are closed to avoid post-dating/pre-dating, thus, we can't introduce more
# transactions. We are experimenting around the Blockchain.

class BaseTransactionBlock(AuditBase):
    '''
    This ledger is for high level, accounts, those that are defined by the system.
    Blocks record and confirm when and in what sequence 
    transactions enter and are logged in the block chain.
    '''
    block_id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=100)
    notes = models.CharField(max_length=160)

    balances_as_at  = models.DateTimeField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.block_id

class BaseTransactionBlockItem(AuditBase):
    balance_amount  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))

    class Meta:
        abstract = True



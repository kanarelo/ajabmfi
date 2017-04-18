from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D
from django.conf import settings

from ajabcapital.apps.core.models import (
    AuditBase, ConfigBase
)

class BaseCustomerProfile(AuditBase):
    #counters
    total_fees_overdue = models.DateTimeField(default=D('0.0'))
    total_principal_overdue = models.DateTimeField(default=D('0.0'))
        
    last_repayment_amount = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    last_repayment_date = models.DateTimeField(null=True)

    first_disbursal_amount = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    first_disbursal_date = models.DateTimeField(null=True)

    last_disbursal_amount = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    last_disbursal_date  = models.DateTimeField(null=True)
    
    class Meta:
        abstract = True

#--------------------------------------------------------------------------------

class IndividualProfile(BaseCustomerProfile):
    FEMALE = 0
    MALE = 1
    
    GENDER = (
        (FEMALE, "Female"),
        (MALE, "Male")
    )
    
    CLIENT = 1
    GROUP_MEMBER = 2
    BUSINESS_STAKEHOLDER = 3

    PROFILE_TYPES = (
        (CLIENT, "Client"),
        (GROUP_MEMBER, "Group Member"),
        (BUSINESS_STAKEHOLDER, "Business Stakeholder"),
    )
    profile_type = models.PositiveIntegerField(choices=PROFILE_TYPES, default=CLIENT)
    user = models.OneToOneField('core_users.User', null=True, blank=True)

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)

    gender = models.PositiveIntegerField(choices=GENDER)

    identity_type = models.ForeignKey('ConfigIdentityType')
    identity_number = models.CharField(max_length=50)
    
    #if the user is blank: not all users can log into the portal
    mobile_phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    last_status = models.ForeignKey('ConfigProfileStatus', null=True)
    last_status_date = models.DateTimeField(null=True)

    def get_full_name(self):
        return "%s %s" % (
            self.first_name, self.last_name
        )

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        db_table = "customer_profile"
        verbose_name = "Individual Profile"

        unique_together = ('identity_number', 'identity_type')

#--------------------------------------------------------------------------------

class GroupProfile(BaseCustomerProfile):
    name = models.CharField(max_length=100)

    loan_group_type = models.ForeignKey('ConfigLoanGroupType', default=1)
    last_group_status = models.ForeignKey('ConfigProfileStatus', null=True)
    last_group_status_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "group_profile"
        verbose_name = "Group Profile"

    def __unicode__(self):
        return self.name

class GroupMembership(AuditBase):
    loan_group_profile = models.ForeignKey('GroupProfile', related_name="members")

    member_individual = models.ForeignKey('IndividualProfile', null=True, related_name="individual_members")
    member_business = models.ForeignKey('BusinessProfile', null=True, related_name="business_members")
    member_group = models.ForeignKey('GroupProfile', null=True, related_name="group_members")

    group_role = models.ForeignKey('ConfigLoanGroupRole')

    class Meta:
        db_table = "group_membership"
        verbose_name = "Group Membership"

    def __unicode__(self):
        return "%s %s" % (self.loan_group_profile, (
                self.member_individual or
                self.member_business or
                self.member_group
            )
        )

    def member(self):
        return (
            self.member_individual or
            self.member_business or
            self.member_group
        )

#--------------------------------------------------------------------------------

class BusinessProfile(BaseCustomerProfile):
    name = models.CharField(max_length=150)

    identity_type = models.ForeignKey('ConfigIdentityType')
    identity_number = models.CharField(max_length=50)

    physical_address = models.CharField(max_length=150)
    location_coodinates = models.CharField(max_length=50)

    last_status = models.ForeignKey('ConfigProfileStatus', null=True)
    last_status_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "business_profile"
        verbose_name = "Business Profile"

        unique_together = ('identity_number', 'identity_type')

    def __unicode__(self):
        return self.name

class BusinessStakeholder(AuditBase):
    business_profile = models.ForeignKey('BusinessProfile', related_name="stakeholders")

    stakeholding_individual = models.ForeignKey('IndividualProfile', null=True, related_name="individual_stakeholder")
    stakeholding_business = models.ForeignKey('BusinessProfile', null=True, related_name="business_stakeholder")
    stakeholding_group = models.ForeignKey('GroupProfile', null=True, related_name="group_stakeholder")

    role = models.ForeignKey('ConfigBusinessRole')

    stake_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "business_stakeholder"
        verbose_name = "Business Stakeholder"

    def __unicode__(self):
        return "%s %s" % (self.business_profile, (
                self.stakeholding_individual or
                self.stakeholding_business or
                self.stakeholding_group
            )
        )

#--------------------------------------------------------------------------------

class ProfileStatus(AuditBase):
    individual_profile  = models.ForeignKey('IndividualProfile', null=True, blank=True)
    business_profile  = models.ForeignKey('BusinessProfile', null=True, blank=True)
    group_profile  = models.ForeignKey('GroupProfile', null=True, blank=True)

    status = models.ForeignKey('ConfigProfileStatus')

    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    class Meta:
        db_table = "profile_status"
        verbose_name = "Profile Status"
        verbose_name_plural = "Profile Statuses"

    def __unicode__(self):
        return "%s %s" % ((
                self.individual_profile or 
                self.business_profile or 
                self.group_profile 
            ), 
            self.status
        )

#--------------------------------------------------------------------------------

class ProfileDocumentUpload(AuditBase):
    individual_profile = models.ForeignKey('IndividualProfile', null=True)
    business_profile = models.ForeignKey('BusinessProfile', null=True)
    group_profile = models.ForeignKey('GroupProfile', null=True)

    document_type = models.ForeignKey('ConfigDocumentType')
    document_uploaded = models.FileField(upload_to="kyc/documents/", db_column="document_path")

    file_upload_reference_number  = models.CharField(max_length=50)
    batch_upload_reference_number = models.CharField(max_length=50)

    file_name = models.CharField(max_length=250)
    file_size = models.DecimalField(max_digits=8, decimal_places=3, default=0)

    remote_browser = models.CharField(max_length=250)
    remote_ip = models.CharField(max_length=30)

    upload_successful = models.BooleanField(default=False)
    upload_period = models.CharField(max_length=8)
    upload_date = models.DateTimeField()
    upload_by = models.ForeignKey('core_users.User', related_name="uploads")

    is_approved = models.NullBooleanField()
    approved_by = models.ForeignKey('core_users.User', related_name="upload_approvals")

    class Meta:
        db_table = "profile_document_upload"
        verbose_name = "Profile Document Upload"

        unique_together = (
            'file_upload_reference_number', 
            'batch_upload_reference_number'
        )

    def __unicode__(self):
        return self.file_name

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)
from django.db import models
from decimal import Decimal as D
from django.conf import settings

from django.utils import timezone

from ajabcapital.apps.core.models import AuditBase, ConfigBase
from ajabcapital.apps.core.auth.codes import *

class UserManager(BaseUserManager):
    """ Custom manager for Member."""

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """ Create and save an Member with the given email and password.
        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.Member user: user
        :raise ValueError: email is not set
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        is_active = extra_fields.pop("is_active", True)

        user = self.model(
            email=email, 
            is_staff=is_staff, 
            is_active=is_active,
            is_superuser=is_superuser, 
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save an Member with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.Member user: regular user
        """
        
        is_staff = extra_fields.pop("is_staff", False)
        
        return self._create_user(
            email, password, is_staff, False, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save an Member with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.Member user: admin user
        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser, PermissionsMixin):
    """ Abstract Member with the same behaviour as Django's default User.
    AbstractMember does not have email field. Uses email as the
    USERNAME_FIELD for authentication.
    Use this if you need to extend Member.
    Inherits from both the AbstractBaseUser and PermissionMixin.
    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser
    """
    
    full_name = models.CharField(max_length=140, null=True, blank=False)

    phone_number = models.CharField(max_length=20, null=True, db_column="mobile_phone_number")
    email = models.EmailField(('email address'), max_length=255, unique=True)

    role = models.PositiveIntegerField(choices=ROLE_CODES, null=False)

    is_staff = models.BooleanField(('staff status'), default=False, help_text=(
            'Designates whether the user can log into the super admin site.'))
    is_active = models.BooleanField(('active'), default=True, help_text=(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))
    
    last_modified = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(('date joined'), 
        auto_now_add=True, db_column="created_at")

    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)
    reason_deleted = models.CharField(max_length=250, null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_deleted_by_me",
        null=True, blank=True, db_column="deleted_by")

    created_by = models.ForeignKey('self', null=True, db_column="created_by")
    row_comment = models.CharField(max_length=250, null=True, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = "user"
        
        verbose_name = ('User')

    def __unicode__(self):
        return self.get_full_name()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.full_name.split()[0] if self.full_name else self.email

    def get_full_name(self):
        return self.full_name or self.get_short_name()

class PasswordToken(AuditBase):
    user = models.ForeignKey('User', related_name="password_tokens")
    token = models.CharField(max_length=256)

    email_sent = models.BooleanField(default=False)

    expiry_date = models.DateTimeField()
    has_expired = models.BooleanField(default=False)

    class Meta:
        db_table = "password_token"

class LogTrail(AuditBase):
    user   = models.ForeignKey('User', related_name="log_trails")
    action = models.CharField(max_length=100)

    class Meta:
        db_table = "log_trail"
        verbose_name = "Log Trail"

class Capability(AuditBase):
    path = models.CharField(max_length=140, unique=True)
    description = models.CharField(max_length=250)

    role_category = models.PositiveIntegerField(choices=ROLE_CATEGORIES)

    def __unicode__(self):
        return "(%s) %s" % (self.path, self.name)

    class Meta:
        db_table = "capability"

        verbose_name = "Capability"
        verbose_name_plural = "Capabilities"

class RoleCapability(AuditBase):
    capability = models.ForeignKey("Capability", related_name="capability_roles")
    
    role_code  = models.PositiveIntegerField(choices=ROLE_CODES)

    is_granted = models.BooleanField(default=False)
        
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="capability_edits", null=False
    )

    def __unicode__(self):
        return "[%s] %s" % (self.role_code, self.capability)

    class Meta:
        db_table = "role_capability"

        unique_together = ("role_code", "capability")

        verbose_name = "Role Capability"
        verbose_name_plural = "Role Capabilities"

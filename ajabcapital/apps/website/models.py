from __future__ import unicode_literals

from django.db import models

class Module(models.Model):
    name = models.CharField(max_length=40)
    initial = models.CharField(max_length=2)
    description = models.CharField(max_length=140)

    is_completed = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    is_buggy = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'website_cms_module'

class Offering(models.Model):
    name  = models.CharField(max_length=40)
    icon  = models.FileField(upload_to="cms/images/")
    description = models.CharField(max_length=140)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'website_cms_offering'

class Page(models.Model):
    title  = models.CharField(max_length=50)
    secondary_title  = models.CharField(max_length=140)
    description = models.CharField(max_length=2000)

    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'website_cms_page'

class Lead(models.Model):
    CHANNELS = (
        (1, "ajab capital marketing"),
        (2, "local tradional media"),
        (3, "a friend/word of mouth"),
        (4, "google"),
        (5, "other"),
    )
    ROLES = (
        (1, "Business Executive"),
        (2, "Technology Executive"),
        (3, "Banking/Loan Executive"),
        (4, "Media Executive"),
    )

    first_name = models.CharField(verbose_name="First Name (required)", max_length=50)
    middle_name = models.CharField(verbose_name="Middle Name", max_length=50)
    sur_name = models.CharField(verbose_name="Surname (required)",  max_length=50)

    email = models.EmailField(verbose_name="Email Address (required)")
    mobile_phone_number = models.CharField(verbose_name="Mobile Phone Number (required)", max_length=20)

    channel = models.IntegerField(verbose_name="How did you hear about us? (required)", choices=CHANNELS)

    company = models.CharField(verbose_name="Your Company (required)", max_length=140)
    role = models.PositiveIntegerField(verbose_name="Your Role (required)", choices=ROLES)

    enrollment_code = models.CharField(max_length=15, unique=True)

    modules = models.ManyToManyField('Module')

    class Meta:
        'crm_leads'

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
        (1, "Local Tradional Media"),
        (2, "A Friend"),
        (3, "Ajab Capital Marketing"),
        (4, "Google"),
        (5, "Other"),
    )
    ROLES = (
        (1, "Managing Director/CEO"),
        (2, "CTO/CIO/IT Director/Manager"),
        (3, "Loan Officer/Administrator"),
        (4, "Staff"),
        (5, "Media"),
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    sur_name = models.CharField(max_length=50)

    email = models.EmailField()
    mobile_phone_number = models.CharField(max_length=20)

    channel = models.IntegerField(verbose_name="How did you hear about us?", choices=CHANNELS)

    company = models.CharField(verbose_name="Your Company", max_length=140)
    role = models.CharField(verbose_name="Your Role", max_length=140, choices=ROLES)

    enrollment_code = models.CharField(max_length=15, unique=True)

    modules = models.ManyToManyField('Module')

    class Meta:
        'crm_leads'

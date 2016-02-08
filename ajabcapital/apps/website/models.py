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
        db_table = 'web_cms_module'

class Offering(models.Model):
    name  = models.CharField(max_length=40)
    icon  = models.FileField(upload_to="cms/images/")
    description = models.CharField(max_length=140)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'web_cms_offering'

class Page(models.Model):
    title  = models.CharField(max_length=50)
    secondary_title  = models.CharField(max_length=140)
    description = models.CharField(max_length=2000)

    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'web_cms_page'
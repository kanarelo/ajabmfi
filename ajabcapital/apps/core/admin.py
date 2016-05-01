from django.contrib import admin

from .models import *

models = globals().copy()

for name, Model in models.iteritems():
    if hasattr(Model, '_meta') and not Model._meta.abstract:
        class Admin(admin.ModelAdmin):
            model = Model

            list_display = [f.name for f in Model._meta.fields[8:]]
            list_filter = [f.name for f in Model._meta.fields[6:9]]
            list_per_page = 25

        admin.site.register(Model, Admin)

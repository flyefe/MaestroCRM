from django.contrib import admin

from .models import Lead, LeadComment

# Register your models here.
admin.site.register(Lead)
admin.site.register(LeadComment)
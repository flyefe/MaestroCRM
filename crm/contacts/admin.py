from django.contrib import admin
from .models import ContactDetail, Log

@admin.register(ContactDetail)
class ContactDetailadmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'tags', 'assigned_staff']  # Customize fields shown in list view


@admin.register(Log)
class Logadmin(admin.ModelAdmin):
    list_display = ['log_type', 'created_by', 'log_title']  # Customize fields shown in list view

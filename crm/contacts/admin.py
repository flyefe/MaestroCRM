from django.contrib import admin
from .models import ContactDetail



@admin.register(ContactDetail)
class ContactDetailadmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'tags', 'assigned_staff']  # Customize fields shown in list view

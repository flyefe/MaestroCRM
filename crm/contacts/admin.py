from django.contrib import admin
from .models import ContactDetail, Status

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Customize the displayed fields as needed

@admin.register(ContactDetail)
class ContactDetailadmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'tags', 'assigned_staff']  # Customize fields shown in list view

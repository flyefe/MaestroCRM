from django.contrib import admin
from .models import ContactDetail, Log

@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'assigned_staff', 'phone_number', 'trafick_source', 'services', 'created_at', 'modified_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number', 'tags')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('contact', 'log_type', 'log_title', 'created_by', 'created_at')
    search_fields = ('contact__user__username', 'log_title', 'log_type', 'created_by__username')

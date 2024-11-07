from django.contrib import admin
from .models import Status, Service, TrafickSource

# Register your models here.
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Customize the displayed fields as needed


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Customize the displayed fields as needed

@admin.register(TrafickSource)
class TrafickSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Customize the displayed fields as needed
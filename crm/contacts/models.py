from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone  # Import this at the top
from settings.models import Status, Service, TrafickSource, Tag



class ContactDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='contact')
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_contacts')
    phone_number = models.CharField(max_length=15, blank=True)

    trafick_source = models.ForeignKey(TrafickSource, on_delete=models.SET_NULL, null=True, blank=True)
    services = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_contacts')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_contacts')

    def __str__(self):
        return f"{self.user.username} - {self.status.name if self.status else 'No Status'}"





class Log(models.Model):
    LOG_TYPE_CHOICES = [
        ('call', 'Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('others', 'Others'),
    ]
    contact = models.ForeignKey(ContactDetail, related_name='log', on_delete=models.CASCADE)
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)  # Options filled in
    log_title = models.CharField(max_length=255)  # Added this field
    log_description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_log', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Set at creation
    modified_at = models.DateTimeField(auto_now=True)      # Updated on save

    def __str__(self):
        return f'commented by {self.created_by.username} on {self.created_at}'

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone

from team.models import Team

SERVICES_CHOICES = [
    ('POF', 'POF'),
    ('Insurance', 'Insurance'),
    ('Visa Processing', 'Visa Processing'),
    ('Admission processing', 'Admission processing'),
    ('Visa fee payment', 'Visa fee payment'),
]

STATUS_CHOICES = [
    ('open', 'Open'),
    ('closed', 'Closed'),
]

class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='FirstName')
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, default='LastName')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    services = models.CharField(max_length=50, choices=SERVICES_CHOICES, default='Visa Processing')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    open_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_clients',
        on_delete=models.CASCADE,
        default=1  # Assuming user with ID 1 exists
    )
    traffic_source = models.CharField(max_length=255, blank=True, null=True)
    converted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='converted_clients',
        on_delete=models.CASCADE,
        default=1  # Assuming user with ID 1 exists
    )
    converted_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)


    class Meta:
        ordering= ('-created_at',)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class ClientComment(models.Model):
    team = models.ForeignKey(Team, related_name='client_comment', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='client_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'commented by {self.created_by.username} on {self.created_at}'

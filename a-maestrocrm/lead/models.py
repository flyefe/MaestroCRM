from django.contrib.auth.models import User
from django.db import models

from team.models import Team

class Lead(models.Model):
    # Lead priority for priority of customers
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    # List to choose from for priority of customers
    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    # Lead property for customer status
    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'
    # List to choose from for customer status
    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )

    team = models.ForeignKey(Team, related_name='leads', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=225)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=MEDIUM)
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
    convert_to_client = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering= ('-created_at',)

    def __str__(self):
        return self.first_name

class LeadComment(models.Model):
    team = models.ForeignKey(Team, related_name='leads_comment', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='lead_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'commented by {self.created_by.username} on {self.created_at}'

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., 'Active', 'Inactive', 'Pending'

    def __str__(self):
        return self.name

class ContactDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(max_length=100, blank=True)  # Comma-separated tags
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_contacts')
    
    def __str__(self):
        return f"{self.user.username} - {self.status.name if self.status else 'No Status'}"

# Signal to automatically assign the Contact group to the user on creation
@receiver(post_save, sender=ContactDetail)
def assign_contact_group(sender, instance, created, **kwargs):
    if created:
        contact_group, _ = Group.objects.get_or_create(name="Contact")
        instance.user.groups.add(contact_group)

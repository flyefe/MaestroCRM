from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        return f"{self.user.username} - {self.contact_status}"
    
    # class Meta:
    #     verbose_name = "Contact Detail"  # Singular form
    #     verbose_name_plural = "Contact Details"  # Plural form

# Signal to automatically create a User and assign to Contact group
@receiver(post_save, sender=ContactDetail)
def create_contact_user(sender, instance, created, **kwargs):
    if created:
        # Create a user with contact-level access
        username = f"{instance.user.first_name}_{instance.user.last_name}".lower()  # Example username
        user = User.objects.create(username=username, first_name=instance.user.first_name, last_name=instance.user.last_name)
        
        # Assign user to 'Contact' group for permissions
        contact_group, _ = Group.objects.get_or_create(name="Contact")
        user.groups.add(contact_group)
        
        # Update the Profile instance with the created user
        instance.user = user
        instance.save()

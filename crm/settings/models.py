from django.db import models
# from django.contrib.auth.models import User, Group
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.



class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., 'Active', 'Inactive', 'Pending'

    def __str__(self):
        return self.name
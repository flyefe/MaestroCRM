from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    max_lead = models.IntegerField()
    max_client = models.IntegerField()

    def __str__(self):
        return self.name
class Team(models.Model):
    plan = models.ForeignKey(Plan, related_name='team', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams') 
    created_by = models.ForeignKey(User, related_name='created_teams', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.name
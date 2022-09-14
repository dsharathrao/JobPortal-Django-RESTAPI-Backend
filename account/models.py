from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile",on_delete=models.CASCADE)
    resume = models.FileField(null=True)

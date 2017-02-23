from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class BaseModel(models.Model):
    class Meta:
        abstract=True


class UserProfile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # user = OneToOneField(User, on_delete=models.CASCADE)
    user_nicename = models.CharField(max_length = 50)
    user_url = models.CharField(max_length=100)
    user_registered = models.DateTimeField(auto_now=True)
    user_status = models.IntegerField(default=0)
    display_name = models.CharField(max_length=250)

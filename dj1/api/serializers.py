from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

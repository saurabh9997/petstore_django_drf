# services/apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Additional fields based on the provided JSON structure
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    user_status = models.IntegerField(default=0)

    def __str__(self):
        return self.username

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('content_manager', 'Content Manager'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=25, choices=ROLES, default='user')
    bio = models.TextField(max_length=500, blank=True)
    country = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('content_manager', 'Content Manager'),
        ('user', 'User'),
    ]

    CONTENT_MODERATION_ROLES = ['admin', 'content_manager', 'editor']

    UPDATE_ANY_POST = ['admin', 'content_manager']

    role = models.CharField(max_length=25, choices=ROLES, default='user')
    bio = models.TextField(max_length=500, blank=True)
    country = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def content_moderator(self):
        return self.role in self.CONTENT_MODERATION_ROLES

    def is_editor(self):
        return self.role == 'editor'
    
    def is_super_updater(self):
        return self.role in self.UPDATE_ANY_POST
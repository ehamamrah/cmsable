import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from apps.core.models import BaseModel
from apps.users.models import User

class PostLanguage(models.TextChoices):
    ENGLISH = 'en', _('English')
    ARABIC = 'ar', _('Arabic')

class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_active_list(cls):
        return cls.objects.filter(active=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class PostCategory(BaseModel):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')
        db_table = 'post_categories'
        verbose_name_plural = 'Post Categories'

class Post(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts', blank=False)
    language = models.CharField(max_length=2, choices=PostLanguage.choices, default=PostLanguage.ARABIC)
    duration = models.DurationField()
    publish_date = models.DateTimeField()
    link = models.URLField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', blank=False, null=False
    )

    def __str__(self):
        return self.title

    def format_duration(self):
        """
        Return the duration in a formatted string (HH:MM:SS)
        """
        total_seconds = int(self.duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
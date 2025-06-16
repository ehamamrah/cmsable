from django.contrib import admin

from .models import Category, Post, PostCategory

from unfold.admin import ModelAdmin

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'language', 'duration', 'publish_date', 'link', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('language', 'publish_date')
    ordering = ('-publish_date',)

@admin.register(PostCategory)
class PostCategoryAdmin(ModelAdmin):
    list_display = ('post', 'category', 'created_at', 'updated_at')
    search_fields = ('post__title', 'category__name')
    list_filter = ('category',)
    ordering = ('post__title',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
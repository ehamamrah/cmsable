from rest_framework import serializers
from django.utils import timezone
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True,
        help_text="List of category UUIDs"
    )
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'categories',
            'category_ids', 'language', 'duration',
            'publish_date', 'link', 'user'
        ]
        read_only_fields = ['id', 'publish_date', 'user', 'categories']

    def create(self, validated_data):
        user = self.context['request'].user
        category_ids = validated_data.pop('category_ids')
        validated_data['publish_date'] = timezone.now()

        if not category_ids:
            raise serializers.ValidationError("Categories are required for a post")
    
        categories = Category.objects.filter(id__in=category_ids)
        if len(categories) != len(category_ids):
            raise serializers.ValidationError("One or more category IDs are invalid")

        post = Post.objects.create(user=user, **validated_data)
        post.categories.set(categories)
        
        return post

    def update(self, instance, validated_data):
        if 'category_ids' in validated_data:
            category_ids = validated_data.pop('category_ids')
            categories = Category.objects.filter(id__in=category_ids)
            if len(categories) != len(category_ids):
                raise serializers.ValidationError("One or more category IDs are invalid")
            instance.categories.set(categories)
        return super().update(instance, validated_data)

from django.urls import path
from apps.posts.views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    CategoriesView
)

urlpatterns = [
    # List posts
    path('', PostListView.as_view(), name='post-list'),
    
    # Create post
    path('create/', PostCreateView.as_view(), name='post-create'),
    
    # Get specific post
    path('<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # Update post
    path('<uuid:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    
    # Delete post
    path('<uuid:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Categories endpoints
    path('categories/', CategoriesView.as_view(), name='categories-list'),
    path('categories/<uuid:pk>/', CategoriesView.as_view(), name='categories-detail'),
] 
from django.urls import path
from apps.posts.views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    CategoriesView,
    PostAutoCreateView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),

    path('create/', PostCreateView.as_view(), name='post-create'),
    path('auto-create/', PostAutoCreateView.as_view(), name='post-auto-create'),

    path('<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('<uuid:pk>/update', PostUpdateView.as_view(), name='post-update'),

    path('<uuid:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    path('categories/', CategoriesView.as_view(), name='categories-list'),
    path('categories/<uuid:pk>/', CategoriesView.as_view(), name='categories-detail'),
] 
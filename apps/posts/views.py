from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsEditorOrReadOnly, IsContentManagerOrReadOnly

class PostListView(generics.ListAPIView):
    """
    View for listing all posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'language']
    search_fields = ['title', 'user__username']
    ordering_fields = ['publish_date', 'title']
    ordering = ['-publish_date']  # Default ordering

    def get_queryset(self):
        queryset = Post.objects.all()

        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

class PostCreateView(generics.CreateAPIView):
    """
    View for creating a new post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PostDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a specific post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class PostUpdateView(generics.UpdateAPIView):
    """
    View for updating a specific post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.user.role in ['admin', 'content_manager']:
            return [IsContentManagerOrReadOnly()]
        return [IsEditorOrReadOnly()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'editor':
            return queryset.filter(user=self.request.user)
        return queryset

class PostDeleteView(generics.DestroyAPIView):
    """
    View for deleting a specific post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.user.role in ['admin', 'content_manager']:
            return [IsContentManagerOrReadOnly()]
        return [IsEditorOrReadOnly()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'editor':
            return queryset.filter(user=self.request.user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.get_active_list()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

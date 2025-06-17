from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .permissions import CanCreatePost, CanUpdatePost, CanDeletePost
from .automated_fetcher.main_reader import MainReader

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'language']
    search_fields = ['title', 'user__username']
    ordering_fields = ['publish_date', 'title']
    ordering = ['-publish_date']

    def get_queryset(self):
        queryset = Post.objects.all()

        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, CanCreatePost]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PostAutoCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, CanCreatePost]

    def create(self, request, *args, **kwargs):
        try:
            # Get the link from request data
            link = request.data.get('link')
            if not link:
                return Response(
                    {'error': 'Link is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            reader = MainReader(link)
            video_info = reader.read()

            post_data = {
                'title': video_info['title'],
                'description': video_info['description'],
                'duration': video_info['duration'],
                'link': link,
                'user': request.user.id,
                'category_ids': request.data.get('category_ids', [])
            }

            serializer = self.get_serializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        try:
            return Post.objects.get(pk=self.kwargs['pk'])
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, CanUpdatePost]
    lookup_field = 'pk'

    def get_object(self):
        try:
            return Post.objects.get(pk=self.kwargs['pk'])
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.user.is_editor():
            return queryset.filter(user=self.request.user)
        return queryset

class PostDeleteView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, CanDeletePost]
    lookup_field = 'pk'

    def get_object(self):
        try:
            return Post.objects.get(pk=self.kwargs['pk'])
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.get_active_list()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class PostDiscoveryView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []  # Empty list means no authentication required
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'language']
    search_fields = ['title', 'user__username']
    ordering_fields = ['publish_date', 'title']
    ordering = ['-publish_date']

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset
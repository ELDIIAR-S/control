from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Comment, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    PostSerializer,
    RegisterSerializer,
    TokenResponseSerializer,
)


def get_visible_posts(user):
    queryset = Post.objects.select_related("author")

    if user.is_authenticated:
        return queryset.filter(
            Q(is_published=True) | Q(author=user)
        )

    return queryset.filter(is_published=True)


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginAPIView(ObtainAuthToken):
    @extend_schema(
        responses={200: TokenResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return get_visible_posts(self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    def get_queryset(self):
        return get_visible_posts(self.request.user)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_post(self):
        return get_object_or_404(
            get_visible_posts(self.request.user),
            pk=self.kwargs["post_id"],
        )

    def get_queryset(self):
        post = self.get_post()

        queryset = Comment.objects.filter(
            post=post,
        ).select_related("author", "post")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(is_approved=True)
                | Q(author=self.request.user)
            )

        return queryset.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(
            post=self.get_post(),
            author=self.request.user,
        )


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Comment.objects.filter(
            post__in=get_visible_posts(self.request.user),
        ).select_related("author", "post")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(is_approved=True)
                | Q(author=self.request.user)
            )

        return queryset.filter(is_approved=True)

    def perform_update(self, serializer):
        serializer.save(is_approved=False)
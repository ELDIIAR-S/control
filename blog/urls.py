from django.urls import path

from .views import (
    CommentDetailAPIView,
    CommentListCreateAPIView,
    LoginAPIView,
    PostDetailAPIView,
    PostListCreateAPIView,
    RegisterAPIView,
)


urlpatterns = [
    path(
        "auth/register/",
        RegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "auth/login/",
        LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "posts/",
        PostListCreateAPIView.as_view(),
        name="post-list",
    ),
    path(
        "posts/<int:pk>/",
        PostDetailAPIView.as_view(),
        name="post-detail",
    ),
    path(
        "posts/<int:post_id>/comments/",
        CommentListCreateAPIView.as_view(),
        name="post-comments",
    ),
    path(
        "comments/<int:pk>/",
        CommentDetailAPIView.as_view(),
        name="comment-detail",
    ),
]
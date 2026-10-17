from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Comment, Post


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        user = User(username=attrs["username"])

        try:
            validate_password(attrs["password"], user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"password": error.messages}
            ) from error

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "title",
            "body",
            "created_at",
            "updated_at",
            "is_published",
        ]
        read_only_fields = [
            "id",
            "author",
            "author_username",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "author_username",
            "body",
            "created_at",
            "updated_at",
            "is_approved",
        ]
        read_only_fields = [
            "id",
            "post",
            "author",
            "author_username",
            "created_at",
            "updated_at",
            "is_approved",
        ]
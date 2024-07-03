import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            img_format, img_str = data.split(";base64,")
            ext = img_format.split("/")[-1]
            data = ContentFile(base64.b64decode(img_str), name="temp." + ext)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Post
        read_only_fields = ("id",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("id", "post")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        read_only=False,
        queryset=User.objects.all(),
    )

    class Meta:
        fields = ["user", "following"]
        model = Follow
        read_only_fields = ("user",)

    def validate_following(self, value):
        curr_user = self.context["request"].user
        following_user = value
        if self.context["request"].user == value:
            raise serializers.ValidationError("Нельзя подписаться на себя!")
        if Follow.objects.filter(
            user=curr_user,
            following=following_user,
        ).exists():
            raise serializers.ValidationError(
                f"Вы уже подписаны на пользователя {following_user}!"
            )
        return value

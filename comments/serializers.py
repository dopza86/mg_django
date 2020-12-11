from rest_framework import serializers
from users.serializers import UserSerializer
from posts.serializers import PostSerializer
from .models import Comment, Text


class TextSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Text
        exclude = ("")


class CommentSerializer(serializers.ModelSerializer):

    post = PostSerializer(read_only=True)
    text = TextSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        exclude = ("")

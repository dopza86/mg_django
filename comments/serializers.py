from rest_framework import serializers
from users.serializers import UserSerializer
from posts.serializers import PostSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ("")

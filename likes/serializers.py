from rest_framework import serializers
from users.serializers import UserSerializer
from posts.serializers import PostSerializer
from .models import Like


class LikeSerializer(serializers.ModelSerializer):

    post = PostSerializer(read_only=True)
    user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Like
        exclude = ("")

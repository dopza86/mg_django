from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("")


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        exclude = ("")

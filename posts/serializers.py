from rest_framework import serializers
from users.serializers import UserSerializer
from likes.serializers import LikeSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from .models import Post, Photo
from likes import models as likes_models


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("")


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    is_liked = serializers.SerializerMethodField()
    like_list = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    def create(self, validated_data):
        tags_list = validated_data.pop('tags')

        request = self.context.get("request")
        images_data = self.context['request'].FILES
        user = request.user
        post = Post.objects.create(**validated_data, user=user)
        post.tags.set(*tags_list)
        for image_data in images_data.getlist('image'):
            Photo.objects.create(post=post, image=image_data)
        post.save()
        return post

    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            try:
                likes_models.Like.objects.get(user__id=request.user.id,
                                              post__id=obj.id)
                return True
            except likes_models.Like.DoesNotExist:
                return False
        return False

    def get_like_list(self, obj):
        request = self.context.get("request")
        if request is not None:
            try:
                result = likes_models.Like.objects.get(post__id=obj.id)
                return LikeSerializer(result).data
            except likes_models.Like.DoesNotExist:
                pass

    class Meta:
        model = Post
        fields = ('id', "user", "photos", "tags", "is_liked", "like_list")

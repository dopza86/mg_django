from rest_framework import serializers
from users.serializers import UserSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from .models import Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("")


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
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

    class Meta:
        model = Post
        exclude = ("")

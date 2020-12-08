from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Post, Photo, Tag


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("")


class TagSerializer(serializers.ModelSerializer):
    post_tag = serializers.SlugRelatedField(many=True,
                                            read_only=True,
                                            slug_field='name')

    class Meta:
        model = Tag
        exclude = ("")


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    tag = serializers.SlugRelatedField(many=True,
                                       queryset=Tag.objects.all(),
                                       slug_field='name')

    def create(self, validated_data):

        tags = validated_data.pop('tag')
        print(tags[0])
        request = self.context.get("request")
        images_data = self.context['request'].FILES
        user = request.user
        post = Post.objects.create(**validated_data, user=user)
        post.tag.set(tags)

        for image_data in images_data.getlist('image'):
            Photo.objects.create(post=post, image=image_data)
        post.save()
        return post

    class Meta:
        model = Post
        exclude = ("")

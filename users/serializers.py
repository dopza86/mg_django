from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from follow_relation import models as follow_models


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    is_follower = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email",
                  "password", "email_secret", "avatar", "is_follower")

    def create(self, validated_data):

        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.verify_email()
        user.save()
        return user

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get("first_name",
                                                 instance.first_name)
        instance.last_name = validated_data.get("last_name",
                                                instance.last_name)
        instance.email = validated_data.get("email", instance.email)

        instance.save()

        return instance

    def get_is_follower(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            try:
                follow_models.FollowRelation.objects.get(
                    follower__id=obj.id, followee__id=request.user.id)
                return True
            except follow_models.FollowRelation.DoesNotExist:
                return False
        return False


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
        )

    def update(self, instance, validated_data):
        instance.password = make_password(
            validated_data.get("password", instance.password))

        instance.save()
        return instance


# class UserPasswordSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "password",)

#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             if attr == 'password':
#                 instance.set_password(value)
#             else:
#                 setattr(instance, attr, value)
#         instance.save()
#         return instance

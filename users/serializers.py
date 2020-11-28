from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "target",
            "follower",
            "password",

        )

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)

        instance.save()

        return instance


class UserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",)

    def update(self, instance, validated_data):
        instance.password = make_password(
            validated_data.get("password", instance.password))
        print(instance.password)

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

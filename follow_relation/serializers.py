from rest_framework import serializers
from users.serializers import UserSerializer

from .models import FollowRelation


class FollowRelationSerializer(serializers.ModelSerializer):

    follower = UserSerializer(read_only=True)
    followee = UserSerializer(read_only=True, many=True)

    class Meta:
        model = FollowRelation
        exclude = ("")

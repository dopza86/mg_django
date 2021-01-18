from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        exclude = ("")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only=True, many=True)

    messages = MessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        exclude = ("")

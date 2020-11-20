from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        exclude = ("")


class ConversationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    message = MessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        exclude = ("")
        read_only_fields = ("user", "message")

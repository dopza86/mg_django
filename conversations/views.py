from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ConversationSerializer
from .models import Conversation

# Create your views here.


class ConversationViewSet(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from .permissions import IsSelf
# Create your views here.


class ConversationSerializer(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def go_conversation(self, request):
        a_pk = request.GET.get("a_pk", None)
        b_pk = request.GET.get("b_pk", None)
        user_one = User.objects.get_or_none(pk=a_pk)
        user_two = User.objects.get_or_none(pk=b_pk)
        queryset = Conversation.objects.all()

        if user_one is not None and user_two is not None:
            try:
                conversation_filter = queryset.filter(participants=user_one.pk)
                conversation = queryset.get(participants=user_two.pk)
                print("conversation:", conversation.pk)

            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create()
                conversation.participants.add(user_one, user_two)

            return redirect(
                f"http://127.0.0.1:8000/api/v1/conversations/{conversation.pk}/"
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)
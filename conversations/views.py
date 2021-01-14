from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from users.models import User
from .permissions import IsSelf, MyMessage


# Create your views here.
class CustomResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class ConversationModelViewSet(ModelViewSet):
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
                serializer = ConversationSerializer(conversation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create()
                conversation.participants.add(user_one, user_two)

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False)
    # def get_conversation(self, request):
    #     a_pk = request.GET.get("a_pk", None)
    #     b_pk = request.GET.get("b_pk", None)
    #     user_one = User.objects.get_or_none(pk=a_pk)
    #     user_two = User.objects.get_or_none(pk=b_pk)
    #     queryset = Conversation.objects.all()

    #     if user_one is not None and user_two is not None:
    #         try:
    #             conversation_filter = queryset.filter(participants=user_one.pk)
    #             conversation = queryset.get(participants=user_two.pk)
    #         return Response(status=status.HTTP_201_CREATED)

    #         except Conversation.DoesNotExist:
    #             return Response(status=status.HTTP_400_BAD_REQUEST)

    #     return Response(status=status.HTTP_400_BAD_REQUEST)


class MessageModelViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [MyMessage]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def send_messages(self, request):
        message = request.data.get("message")
        pk = request.GET.get("pk", None)
        conversation = Conversation.objects.get_or_none(pk=pk)

        print(conversation)
        if request.user.is_authenticated:
            if not conversation:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if message is not None:
                Message.objects.create(message=message,
                                       user=self.request.user,
                                       conversation=conversation)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, UserPasswordSerializer
from .models import User
from django.contrib.auth.hashers import make_password


# Create your views here.


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["put"])
    def update_user(self, request, pk):
        user = User.objects.get(pk=pk)

        if user is not None:
            serializer = UserSerializer(
                user, data=request.data, partial=True)

            if serializer.is_valid():
                user = serializer.save()

                return Response(UserSerializer(user).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["put"])
    def update_password(self, request, pk):
        user = User.objects.get(pk=pk)

        if user is not None:
            serializer = UserPasswordSerializer(
                user, data=request.data, partial=True)

            if serializer.is_valid():

                user = serializer.save()

                return Response(UserPasswordSerializer(user).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

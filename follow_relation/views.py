from django.shortcuts import render
from django.db import IntegrityError

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .serializers import FollowRelationSerializer
from .models import FollowRelation
from users.models import User
from .permissions import IsSelf

# Create your views here.


class FollowRelationViewSet(ModelViewSet):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowRelationSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=True)
    @permission_classes([IsAuthenticated])
    def follow(self, request, pk):
        user = request.user

        if user.id is not None:
            try:
                FollowRelation.objects.get(follower=user)
            except FollowRelation.DoesNotExist:
                FollowRelation.objects.create(follower=user)
                return Response(status=status.HTTP_200_OK)

            target = FollowRelation.objects.get(follower=user).followee
            target_user = User.objects.get(pk=pk)
            if user == target_user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if target_user in target.all():
                target.remove(target_user)
            else:
                target.add(target_user)
            FollowRelation.objects.get(follower=user).save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
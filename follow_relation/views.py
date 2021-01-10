from django.shortcuts import render
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

    @action(detail=False)
    @permission_classes([IsAuthenticated])
    def follow(self, request):
        user = request.user
        follow_pk = request.GET.get("follow_pk", None)
        target_user = User.objects.get(pk=follow_pk)
        if user.id is not None:
            try:
                FollowRelation.objects.get(follower=target_user)
            except FollowRelation.DoesNotExist:
                FollowRelation.objects.create(follower=target_user)

            target = FollowRelation.objects.get(follower=target_user).followee

            if user == target_user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if user in target.all():
                target.remove(user)
            else:
                target.add(user)
            FollowRelation.objects.get(follower=target_user).save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    @permission_classes([IsAuthenticated])
    def my_follow(self, request):
        user = request.user

        result = FollowRelation.objects.get(follower=user)
        serializer = FollowRelationSerializer(result)

        return Response(serializer.data)
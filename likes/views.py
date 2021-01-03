from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from users.models import User

from .serializers import LikeSerializer
from .models import Like
from .permissions import IsSelf

# Create your views here.


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

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
    def handle_like(self, request):
        user = request.user
        post_pk = request.GET.get("post_pk", None)
        post = Post.objects.get_or_none(pk=post_pk)
        if post is not None:
            try:
                Like.objects.get(post=post)
            except Like.DoesNotExist:
                Like.objects.create(post=post)

            target = Like.objects.get(post=post).user
            target_user = user
            if target_user in target.all():
                target.remove(target_user)
            else:
                target.add(target_user)
            Like.objects.get(post=post)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def post_like(self, request):
        user = request.user
        post_pk = request.GET.get("post_pk", None)
        post = Post.objects.get_or_none(pk=post_pk)
        if post is not None:
            result = Like.objects.get(post=post)
            serializer = LikeSerializer(result)
            print(serializer.data)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
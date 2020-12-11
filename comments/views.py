from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Post
from .serializers import CommentSerializer, TextSerializer
from .models import Comment, Text
from .permissions import IsSelf, MyText
# Create your views here.


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def go_comment(self, request):
        user = request.user
        pk = request.GET.get("pk", None)
        post = Post.objects.get_or_none(pk=pk)
        queryset = Comment.objects.all()
        if post is not None:
            try:
                comment = queryset.get(post=post)
            except Comment.DoesNotExist:
                comment = Comment.objects.create(post=post)
            return redirect(
                f"http://127.0.0.1:8000/api/v1/comments/text/write_text/?pk={comment.pk}"
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TextViewSet(ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [MyText]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def write_text(self, request):
        user = request.user
        text = request.data.get("text")
        pk = request.GET.get("pk", None)

        comment = Comment.objects.get_or_none(pk=pk)

        if request.user.is_authenticated:
            if not text:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if text is not None:
                Text.objects.create(text=text, user=user, comment=comment)

            return redirect(
                f"http://127.0.0.1:8000/api/v1/comments/comments/{comment.pk}/"
            )
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

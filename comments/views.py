from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.models import Post
from .serializers import CommentSerializer
from .models import Comment
from .permissions import IsSelf
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

    @action(methods=["post"], detail=False)
    def go_comment(self, request):
        user = request.user
        
        pk = request.GET.get("post_pk", None)
        post = Post.objects.get_or_none(pk=pk)
        print(post)
        if post is not None:
            text = request.data.get("text")
            print(text)
            comment = Comment.objects.create(post=post, user=user, text=text)
            serializer = CommentSerializer(comment).data

            return Response(data=serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False)
    def get_comment(self, request):

        user = request.user
        post_pk = request.GET.get("post_pk", None)
        post = Post.objects.get_or_none(pk=post_pk)
        paginator = self.paginator
        if post is not None:
            filter_kwargs = {}
            filter_kwargs["post"] = post
            posts = Comment.objects.filter(**filter_kwargs).order_by('-id')
            results = paginator.paginate_queryset(posts, request)
            serializer = CommentSerializer(results, read_only=True, many=True)

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
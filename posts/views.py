from django.shortcuts import render
from rest_framework.decorators import action, permission_classes
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import Post
from .permissions import IsSelf

# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(methods=["post"], detail=False)
    def search(self, request):
        name = request.data.get("name", None)
        location = request.data.get("location", None)
        caption = request.data.get("caption", None)
        user = request.data.get("user", None)
        tags = request.data.get("tags", None)
        print(user)
        filter_kwargs = {}

        if user is not None:
            filter_kwargs["user"] = user
            posts = Post.objects.filter(user__username=user).distinct()
            paginator = self.paginator
            results = paginator.paginate_queryset(posts, request)
            print(results)
            serializer = PostSerializer(results,
                                        many=True,
                                        context={"request": request})

            return paginator.get_paginated_response(serializer.data)
        if tags is not None:
            filter_kwargs["tags"] = tags
            hashtags = tags.split(",")
            paginator = self.paginator
            posts = Post.objects.filter(tags__name__in=hashtags).distinct()
            results = paginator.paginate_queryset(posts, request)
            print(results)
            serializer = PostSerializer(results,
                                        many=True,
                                        context={"request": request})

            return paginator.get_paginated_response(serializer.data)

        else:
            if name is not None:
                filter_kwargs["name__istartswith"] = name
            if location is not None:
                filter_kwargs["location__icontains"] = location
            if caption is not None:
                filter_kwargs["caption__istartswith"] = caption

            paginator = self.paginator
            try:
                posts = Post.objects.filter(**filter_kwargs)
            except ValueError:
                posts = Post.objects.all()

            results = paginator.paginate_queryset(posts, request)
            print(results)
            serializer = PostSerializer(results,
                                        many=True,
                                        context={"request": request})
            return paginator.get_paginated_response(serializer.data)

    # @action(detail=False, methods=["post"])
    # @permission_classes([permissions.IsAuthenticated])
    # def create_post(self, request):
    #     user = request.user
    #     tag = self.validated_data

    #     return Response(status=status.HTTP_200_OK)
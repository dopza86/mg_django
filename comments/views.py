from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CommentSerializer
from .models import Comment

# Create your views here.


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

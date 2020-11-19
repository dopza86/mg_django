from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import LikeSerializer
from .models import Like

# Create your views here.


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

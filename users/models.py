from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):

    email = models.EmailField(verbose_name="이메일", null=True, blank=True)
    last_name = models.CharField(
        verbose_name="성", max_length=50, null=True, blank=True)
    first_name = models.CharField(
        verbose_name="이름", max_length=50, null=True, blank=True)
    bio = models.TextField(verbose_name="소개", default="", blank=True)
    target = models.ManyToManyField(
        "users.User", verbose_name="팔로잉", related_name="followers")
    follower = models.ManyToManyField(
        "users.User", verbose_name="팔로워", related_name="targets")

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

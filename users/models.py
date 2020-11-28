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
        "users.User", verbose_name="팔로잉",  null=True, blank=True, related_name="followers")
    follower = models.ManyToManyField(
        "users.User", verbose_name="팔로워",  null=True, blank=True, related_name="targets")

    def following_count(self):
        following_count = self.target.count()
        return following_count
    following_count.short_description = "팔로잉"

    def follower_count(self):
        follower_count = self.follower.count()
        return follower_count
    follower_count.short_description = "팔로워"

    def post_count(self):
        post_count = self.post_user.count()
        return post_count
    post_count.short_description = "포스트"

    def like_count(self):
        like_count = self.likes.count()
        return like_count
    like_count.short_description = "좋아요"

    def comment_count(self):
        comment_count = self.comments.count()
        return comment_count
    comment_count.short_description = "작성댓글"

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

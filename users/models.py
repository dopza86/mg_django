import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
# Create your models here.


class User(AbstractUser):
    LOGIN_WEB = "web"
    LOGIN_KAKAO = "kakao"
    LOGIN_GOOGLE = "google"

    LOGIN_CHOICES = (
        (LOGIN_WEB, "웹"),
        (LOGIN_KAKAO, "카카오"),
        (LOGIN_GOOGLE, "구글"),
    )

    login_method = models.CharField(
        verbose_name="로그인 방법", max_length=50, choices=LOGIN_CHOICES, default=LOGIN_WEB
    )

    email = models.EmailField(verbose_name="이메일", null=True, blank=True)
    last_name = models.CharField(
        verbose_name="성", max_length=50, null=True, blank=True)
    first_name = models.CharField(
        verbose_name="이름", max_length=50, null=True, blank=True)
    bio = models.TextField(verbose_name="소개", default="", blank=True)
    target = models.ManyToManyField(
        "users.User", verbose_name="팔로잉", blank=True, related_name="followers")
    follower = models.ManyToManyField(
        "users.User", verbose_name="팔로워", blank=True, related_name="targets")
    avatar = models.ImageField(
        verbose_name="사진", upload_to="avatars", blank=True)
    email_verified = models.BooleanField(verbose_name="메일인증", default=False)
    email_secret = models.CharField(
        verbose_name="메일인증키", max_length=20, default="", blank=True)

    def verify_email(self):

        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret})
            # html 을 스트링으로 바꾼다
            send_mail(
                ("마이비앤비 가입 인증메일 입니다"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()

        return

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

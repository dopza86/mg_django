from django.db import models
from core import models as core_models


class Comment(core_models.TimeStampedModel):
    post = models.ForeignKey(
        "posts.Post", related_name="comments", blank=True, on_delete=models.CASCADE)
    users = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="댓글", blank=True, null=True)

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글"

from django.db import models
from core import models as core_models


class Like(core_models.TimeStampedModel):
    posts = models.OneToOneField(
        "posts.Post", related_name="Likes", blank=True, on_delete=models.CASCADE)
    users = models.ManyToManyField("users.User", related_name="Likes")

    def count_users(self):
        return self.users.count()
    count_users.short_description = "좋아요 갯수"

    class Meta:
        verbose_name = "좋아요"
        verbose_name_plural = "좋아요"

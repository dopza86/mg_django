from django.db import models
from core import models as core_models


class Like(core_models.TimeStampedModel):
    post = models.OneToOneField(
        "posts.Post", related_name="likes", blank=True, on_delete=models.CASCADE)
    user = models.ManyToManyField("users.User", related_name="likes")

    def count_users(self):
        return self.user.count()
    count_users.short_description = "좋아요 갯수"

    class Meta:
        verbose_name = "좋아요"
        verbose_name_plural = "좋아요"

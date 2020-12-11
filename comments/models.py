from django.db import models
from core import models as core_models


class Text(core_models.TimeStampedModel):

    text = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey("users.User",
                             related_name="text",
                             on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment",
                                related_name="text",
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "텍스트"
        verbose_name_plural = "텍스트"


class Comment(core_models.TimeStampedModel):

    post = models.ForeignKey("posts.Post",
                             verbose_name="포스트",
                             related_name="comment",
                             on_delete=models.CASCADE,
                             blank=True)

    def __str__(self):
        return self.post.name

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글"

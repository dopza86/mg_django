from django.db import models
from core import models as core_models


class Comment(core_models.TimeStampedModel):

    text = models.TextField()
    user = models.ForeignKey("users.User",
                             related_name="comment",
                             on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post",
                             related_name="comment",
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "커멘트"
        verbose_name_plural = "커멘트"

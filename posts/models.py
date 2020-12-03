from django.db import models
from core import models as core_models
# Create your models here.


class Post(core_models.TimeStampedModel):
    name = models.CharField(verbose_name="이름",
                            max_length=140,
                            null=True,
                            blank=True)
    location = models.CharField(verbose_name="위치", max_length=256)
    caption = models.TextField(default="", verbose_name="설명", blank=True)
    user = models.ForeignKey("users.User",
                             on_delete=models.CASCADE,
                             related_name="post_user")

    def count_comment(self):
        count_comment = self.comments.count()

        return count_comment

    count_comment.short_description = "댓글"

    def count_like(self):
        count_like = self.likes.user.count()

        return count_like

    count_like.short_description = "좋아요"

    class Meta:
        verbose_name = "포스트"
        verbose_name_plural = "포스트"

    def __str__(self):
        return self.name


class Photo(core_models.TimeStampedModel):
    file = models.ImageField(verbose_name="사진 파일",
                             upload_to="post_images",
                             blank=True,
                             null=True)
    post = models.ForeignKey("posts.Post",
                             related_name="photos",
                             on_delete=models.CASCADE)
    caption = models.CharField(max_length=140)

    def __str__(self):
        return self.post.name

    class Meta:
        verbose_name = "사진"
        verbose_name_plural = "사진"

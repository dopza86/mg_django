from django.db import models
from core import models as core_models


class FollowRelation(core_models.TimeStampedModel):
    follower = models.OneToOneField("users.User",
                                    verbose_name="유저",
                                    related_name='follower',
                                    on_delete=models.CASCADE)
    followee = models.ManyToManyField("users.User",
                                      verbose_name="팔로워",
                                      blank=True,
                                      related_name='followee')

    def count_followee(self):
        return self.followee.count()

    count_followee.short_description = "팔로잉 유저"

    class Meta:
        verbose_name = "팔로우"
        verbose_name_plural = "팔로우"

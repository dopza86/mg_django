from django.db import models
from . import managers


class TimeStampedModel(models.Model):

    created = models.DateTimeField(verbose_name="생성 일시", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="추가 일시", auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True

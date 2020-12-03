from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    list_display = ("follower", )

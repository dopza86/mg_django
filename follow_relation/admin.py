from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    list_per_page = 10

    list_display = ("follower", "count_followee")

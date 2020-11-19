from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.Post)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "location",
        "caption",
        "user", "count_photos",)

    fieldsets = (
        ("포스트", {"fields": ("name", "location", "caption", "user")},),)

    def count_photos(self, obj):

        return str(obj.photos.count())

    count_photos.short_description = "사진 갯수"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "post",
    )

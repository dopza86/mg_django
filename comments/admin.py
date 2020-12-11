from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ("post", )


@admin.register(models.Text)
class TextAdmin(admin.ModelAdmin):

    list_display = ("user", "comment")

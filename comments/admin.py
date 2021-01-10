from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_per_page = 10

    list_display = ("post", "text", "user")

from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ("post", "users", "text")

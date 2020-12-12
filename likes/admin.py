from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_per_page = 10

    list_display = ("post", "count_users")
    filter_horizontal = ("user", )

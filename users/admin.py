from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.


@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + \
        (("커스텀프로필", {"fields": ("bio", "target", "follower")},),)
    list_display = UserAdmin.list_display
    list_filter = UserAdmin.list_filter

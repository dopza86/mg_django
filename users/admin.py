from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

from . import models
# Register your models here.


@admin.register(models.User)
class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_per_page = 10
    fieldsets = UserAdmin.fieldsets + \
        (("커스텀프로필", {"fields": ("login_method", "bio","email_verified",
                                "email_secret",
                                "avatar")},),)
    list_display = UserAdmin.list_display + (
        "login_method",
        "post_count",
        "like_count",
        # "comment_count",
        "email_verified",
        "email_secret",
    )
    list_filter = UserAdmin.list_filter

    search_fields = ("username", )

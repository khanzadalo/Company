from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from apps.users.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", 'email', "is_staff", "is_active", "is_admin")
    list_display_links = ("username",)
    list_filter = ("is_active", "is_staff", "is_admin", "created_at")
    list_editable = ("is_active", "is_staff")
    readonly_fields = ("created_at", "last_login")
    search_fields = ("username",)
    ordering = ('-created_at',)
    list_per_page = 25
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    'email',
                    "password",
                    'otp',
                    "is_admin",
                    "is_staff",
                    "is_active",
                    "created_at",
                    "last_login",
                )
            },
        ),
    )

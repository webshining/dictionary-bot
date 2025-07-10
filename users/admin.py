from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        "username",
        "telegram_id",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (
            "Admin",
            {
                "fields": (
                    "username",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Telegram Info",
            {
                "fields": (
                    "telegram_id",
                    "first_name",
                    "last_name",
                    "telegram_username",
                    "language_code",
                )
            },
        ),
    )

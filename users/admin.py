from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Настройка отображения кастомной модели пользователя в админке."""

    list_display = ("id", "avatar_preview", "email", "username", "phone", "country", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "country")
    search_fields = ("email", "username", "phone", "country")
    ordering = ("email",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {"fields": ("avatar", "phone", "country")},
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Дополнительная информация",
            {"fields": ("email", "avatar", "phone", "country")},
        ),
    )

    def avatar_preview(self, obj):
        """Миниатюра аватара прямо в списке."""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; '
                'object-fit: cover; border-radius: 50%;" />',
                obj.avatar.url,
            )
        return format_html('<span style="color: #999; font-size: 11px;">{}</span>', "Нет фото")

    avatar_preview.short_description = "Аватар"

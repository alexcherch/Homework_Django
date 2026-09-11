from django.contrib import admin
from django.utils.html import format_html

from catalog.models import Category, ContactInfo, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""

    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения продуктов в админке"""

    list_display = ("id", "image_preview", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")

    def image_preview(self, obj):
        """Метод для генерации миниатюры картинки прямо в таблице админки"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return format_html('<span style="color: #999; font-size: 11px;">{}</span>', "Нет фото")

    image_preview.short_description = "Превью"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Настройка отображения контактов в админке"""

    list_display = ("id", "address", "phone", "email")

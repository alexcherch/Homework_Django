from django.contrib import admin

from catalog.models import Category, ContactInfo, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админ-панели"""

    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения продуктов в админ-панели"""

    list_display = ("id", "name", "price", "category")

    list_filter = ("category",)

    search_fields = ("name", "description")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Настройка отображения контактов в админке"""

    list_display = ("id", "address", "phone", "email")

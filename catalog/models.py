from django.db import models


class Category(models.Model):
    """Модель категории товаров"""

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание категории",
    )

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта (товара)"""

    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование товара",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание товара",
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products",
        help_text="Выберите категорию товара",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Укажите цену товара",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    """Модель для хранения контактных данных компании"""

    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.CharField(max_length=100, verbose_name="Email")

    class Meta:
        verbose_name = "контактные данные"
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return f"Контакты: {self.phone} | {self.email}"

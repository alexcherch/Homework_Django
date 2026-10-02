from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования товара с кастомной валидацией"""

    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price", "is_published"]

    def __init__(self, *args, user=None, **kwargs):
        """Стилизация полей + скрытие is_published для не-модераторов"""
        super().__init__(*args, **kwargs)
        self.user = user

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control py-2"

        if self.user and self.user.is_authenticated:
            is_moderator = self.user.groups.filter(name="Модератор продуктов").exists() or self.user.is_superuser
            if not is_moderator:
                self.fields.pop("is_published", None)
        else:
            self.fields.pop("is_published", None)

    def clean_price(self):
        """Валидация цены: защита от отрицательных значений по ТЗ"""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной! Укажите корректную стоимость.")
        return price

    def clean_name(self):
        """Валидация названия на отсутствие запрещенных слов (без учета регистра)"""
        name = self.cleaned_data.get("name")
        name_lower = name.lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(f"Запрещено использовать слово '{word}' в названии товара!")
        return name

    def clean_description(self):
        """Валидация описания на отсутствие запрещенных слов (без учета регистра)"""
        description = self.cleaned_data.get("description")
        description_lower = description.lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description_lower:
                raise ValidationError(f"Запрещено использовать слово '{word}' в описании товара!")
        return description

    def clean_image(self):
        """Валидация изображения: проверка формата (JPEG/PNG) и размера (до 5 МБ) по ТЗ"""
        image = self.cleaned_data.get("image")

        if not image:
            return image

        max_size_bytes = 5 * 1024 * 1024
        if image.size > max_size_bytes:
            raise ValidationError("Размер файла превышает 5 МБ! Пожалуйста, сожмите изображение или выберите другое.")

        import os

        ext = os.path.splitext(image.name)[1].lower()
        valid_extensions = [".jpg", ".jpeg", ".png"]

        if ext not in valid_extensions:
            raise ValidationError(
                "Неподдерживаемый формат файла! Допускаются только изображения в формате JPEG или PNG."
            )

        return image

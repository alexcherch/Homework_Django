from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Кастомная команда для полной очистки БД и загрузки тестовых данных из фикстур"""

    help = "Очищает базу данных и загружает тестовые данные из JSON фикстур."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Очистка таблиц продуктов и категорий..."))
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Таблицы успешно очищены."))

        fixtures_dir = Path(__file__).resolve().parent.parent.parent / "fixtures"
        categories_fixture = fixtures_dir / "categories.json"
        products_fixture = fixtures_dir / "products.json"

        if categories_fixture.exists():
            self.stdout.write("Загрузка категорий из фикстуры...")
            call_command("loaddata", str(categories_fixture))
            self.stdout.write(self.style.SUCCESS("Категории успешно загружены."))
        else:
            self.stdout.write(self.style.ERROR(f"Файл фикстуры {categories_fixture} не найден!"))

        if products_fixture.exists():
            self.stdout.write("Загрузка продуктов из фикстуры...")
            call_command("loaddata", str(products_fixture))
            self.stdout.write(self.style.SUCCESS("Продукты успешно загружены."))
        else:
            self.stdout.write(self.style.ERROR(f"Файл фикстуры {products_fixture} не найден!"))

        self.stdout.write(self.style.SUCCESS("=== БАЗА ДАННЫХ ИНТЕРНЕТ-МАГАЗИНА УСПЕШНО ОБНОВЛЕНА ==="))

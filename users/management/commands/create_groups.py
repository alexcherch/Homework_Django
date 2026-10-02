from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создаёт группы пользователей с нужными правами.

    Использование:
        python manage.py create_groups
    """

    help = "Создаёт группы 'Модератор продуктов' и 'Контент-менеджер' с нужными правами"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Создание групп и назначение прав..."))

        moderators_group, created = Group.objects.get_or_create(name="Модератор продуктов")
        if created:
            self.stdout.write(self.style.SUCCESS("  [+] Создана группа 'Модератор продуктов'"))
        else:
            self.stdout.write("  [=] Группа 'Модератор продуктов' уже существует")

        product_ct = ContentType.objects.get(app_label="catalog", model="product")
        can_unpublish = Permission.objects.get(
            content_type=product_ct,
            codename="can_unpublish_product",
        )
        delete_product = Permission.objects.get(
            content_type=product_ct,
            codename="delete_product",
        )
        moderators_group.permissions.set([can_unpublish, delete_product])
        self.stdout.write(self.style.SUCCESS("      Права назначены: can_unpublish_product, delete_product"))

        content_group, created = Group.objects.get_or_create(name="Контент-менеджер")
        if created:
            self.stdout.write(self.style.SUCCESS("  [+] Создана группа 'Контент-менеджер'"))
        else:
            self.stdout.write("  [=] Группа 'Контент-менеджер' уже существует")

        blog_ct = ContentType.objects.get(app_label="blog", model="blogpost")
        blog_perms = Permission.objects.filter(
            content_type=blog_ct,
            codename__in=[
                "add_blogpost",
                "change_blogpost",
                "delete_blogpost",
                "view_blogpost",
            ],
        )
        content_group.permissions.set(blog_perms)
        self.stdout.write(
            self.style.SUCCESS("      Права назначены: add/change/delete/view_blogpost")
        )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Готово!"))

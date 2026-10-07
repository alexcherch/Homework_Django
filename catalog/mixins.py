from django.contrib.auth.mixins import UserPassesTestMixin


class ProductOwnerOrModeratorMixin(UserPassesTestMixin):
    """Миксин для проверки прав на редактирование/удаление товара.

    Доступ разрешён:
      - владельцу товара (product.owner == user)
      - модератору (состоит в группе «Модератор продуктов»)
      - суперпользователю
    """

    def test_func(self):
        """Проверяем, что пользователь — владелец товара, модератор или суперюзер."""
        product = self.get_object()
        user = self.request.user
        is_moderator = user.groups.filter(name="Модератор продуктов").exists()
        return user == product.owner or is_moderator or user.is_superuser

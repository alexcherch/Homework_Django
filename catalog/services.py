from django.core.cache import cache

from catalog.models import Category, Product

CATEGORY_PRODUCTS_CACHE_KEY = "category_{category_id}"
CATEGORY_PRODUCTS_CACHE_TTL = 600  # 10 минут


def get_products_by_category(category_id: int):
    """Возвращает список опубликованных товаров указанной категории.

    Логика:
        1. Пытаемся получить данные из кеша по ключу `category_{id}`.
        2. Если в кеше нет — идём в БД, кладём результат в кеш с TTL.
        3. Если категории нет — возвращаем пустой queryset.

    Args:
        category_id: ID категории, товары которой нужно получить.

    Returns:
        QuerySet/список объектов Product.
    """
    cache_key = CATEGORY_PRODUCTS_CACHE_KEY.format(category_id=category_id)

    products = cache.get(cache_key)
    if products is not None:
        return products

    if not Category.objects.filter(pk=category_id).exists():
        return Product.objects.none()

    products = list(
        Product.objects.filter(category_id=category_id, is_published=True)
        .select_related("category", "owner")
        .order_by("name")
    )

    cache.set(cache_key, products, timeout=CATEGORY_PRODUCTS_CACHE_TTL)
    return products


def invalidate_category_cache(category_id: int):
    """Сбрасывает кеш товаров указанной категории.

    Используется при создании/редактировании/удалении товаров,
    чтобы кеш не отдавал устаревшие данные.
    """
    cache.delete(CATEGORY_PRODUCTS_CACHE_KEY.format(category_id=category_id))


def invalidate_products_list_cache():
    """Сбрасывает все ключи кеша списка товаров (главной страницы).

    Сбрасываем все возможные варианты:
        - products_list_all_page_1, products_list_all_page_2, ...
        - products_list_{category_id}_page_1, products_list_{category_id}_page_2, ...
    """
    from catalog.models import Category

    for page in range(1, 21):
        cache.delete(f"products_list_all_page_{page}")

    for category in Category.objects.all():
        for page in range(1, 21):
            cache.delete(f"products_list_{category.pk}_page_{page}")

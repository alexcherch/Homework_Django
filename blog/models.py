from django.db import models


class BlogPost(models.Model):
    """Модель блоговой записи (статьи)"""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(
        max_length=200, verbose_name="slug", blank=True, null=True
    )
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(
        upload_to="blog/", verbose_name="Превью (изображение)", blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    is_published = models.BooleanField(
        default=True, verbose_name="Признак публикации"
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

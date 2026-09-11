from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.models import BlogPost


class BlogPostListView(ListView):
    """Контроллер списка статей"""

    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"

    def get_queryset(self):
        """Выводим только те статьи, которые имеют положительный признак публикации"""
        return super().get_queryset().filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Контроллер детального просмотра статьи"""

    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров и отправляем email при достижении 100 просмотров"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        if obj.views_count == 100:
            subject = f"Поздравляем! Статья '{obj.title}' достигла успеха!"
            message = (
                f"Ура! Ваша блоговая запись '{obj.title}' набрала ровно 100 просмотров. " f"Продолжайте в том же духе!"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )

        return obj


class BlogPostCreateView(CreateView):
    """Контроллер создания статьи"""

    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:list")


class BlogPostUpdateView(UpdateView):
    """Контроллер редактирования статьи"""

    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blog_form.html"

    def get_success_url(self):
        """После успешного редактирования перенаправляем на страницу отредактированной статьи"""
        return reverse("blog:detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Контроллер удаления статьи"""

    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:list")

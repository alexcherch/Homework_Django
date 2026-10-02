from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер создания статьи (только для контент-менеджеров)"""

    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:list")
    permission_required = "blog.add_blogpost"


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер редактирования статьи (только для контент-менеджеров)"""

    model = BlogPost
    fields = ["title", "content", "image", "is_published"]
    template_name = "blog/blog_form.html"
    permission_required = "blog.change_blogpost"

    def get_success_url(self):
        """После успешного редактирования перенаправляем на страницу отредактированной статьи"""
        return reverse("blog:detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер удаления статьи (только для контент-менеджеров)"""

    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
    permission_required = "blog.delete_blogpost"

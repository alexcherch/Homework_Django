from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm


class RegisterView(CreateView):
    """Регистрация нового пользователя и отправка приветственного письма."""

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Сохраняем пользователя, шлём письмо, редиректим на страницу входа."""
        # Автозаполнение username значением email
        # (username остаётся в модели, но в форме его нет — ТЗ требует только email и пароль)
        form.instance.username = form.cleaned_data["email"]

        user = form.save()

        send_mail(
            subject="Добро пожаловать в Skypro Shop!",
            message=(
                f"Здравствуйте!\n\n"
                f"Спасибо за регистрацию на нашем сайте.\n"
                f"Ваш email для входа: {user.email}\n\n"
                f"Хороших покупок!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class LoginView(BaseLoginView):
    """Вход по email и паролю с кастомной формой."""

    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True


class LogoutView(BaseLogoutView):
    """Выход из системы."""

    next_page = reverse_lazy("users:login")


class ProfileView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля текущего пользователя."""

    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Возвращаем текущего пользователя — редактируем только свой профиль."""
        return self.request.user

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from catalog.forms import ProductForm
from catalog.mixins import ProductOwnerOrModeratorMixin
from catalog.models import Category, ContactInfo, Product


class ProductListView(ListView):
    """Контроллер для отображения главной страницы (список товаров)"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        category_id = self.request.GET.get("category")
        if category_id:
            context["selected_category"] = int(category_id)
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения детальной информации о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания нового товара"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_kwargs(self):
        """Передаём текущего пользователя в форму (для проверки прав на is_published)"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Автоматически привязываем товар к текущему пользователю"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, ProductOwnerOrModeratorMixin, UpdateView):
    """Контроллер для редактирования товара (только владелец или модератор)"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_kwargs(self):
        """Передаём текущего пользователя в форму (для проверки прав на is_published)"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProductDeleteView(LoginRequiredMixin, ProductOwnerOrModeratorMixin, DeleteView):
    """Контроллер для удаления товара (владелец, модератор или суперюзер)"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Отмена публикации товара. Доступно только модераторам с правом can_unpublish_product."""

    permission_required = "catalog.can_unpublish_product"
    raise_exception = True

    def post(self, request, *args, **kwargs):
        """Отменяем публикацию и возвращаемся на страницу товара."""
        product = get_object_or_404(Product, pk=kwargs["pk"])
        product.is_published = False
        product.save(update_fields=["is_published", "updated_at"])
        return redirect("catalog:product_detail", pk=product.pk)


class ContactsTemplateView(TemplateView):
    """Контроллер для страницы контактов"""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_data"] = ContactInfo.objects.first()
        context["success"] = False
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print("\n=== ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (CBV) ===")
        print(f"Имя: {name} | Email: {email} | Сообщение: {message}\n")

        context = self.get_context_data()
        context["success"] = True
        return self.render_to_response(context)

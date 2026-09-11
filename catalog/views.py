from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from catalog.models import Category, ContactInfo, Product


class ProductListView(ListView):
    """Контроллер для отображения главной страницы (список товаров)"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        """Фильтрация товаров по выбранной категории"""
        queryset = super().get_queryset().order_by("id")
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        """Передаем список категорий и id выбранной категории в шаблон"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        category_id = self.request.GET.get("category")
        if category_id:
            context["selected_category"] = int(category_id)
        return context


class ProductDetailView(DetailView):
    """Контроллер для отображения детальной информации о товаре"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Контроллер для создания нового товара через форму"""

    model = Product
    fields = ["name", "description", "image", "category", "price"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ContactsTemplateView(TemplateView):
    """Контроллер для страницы контактов"""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_data"] = ContactInfo.objects.first()
        context["success"] = False
        return context

    def post(self, request, *args, **kwargs):
        """Обработка отправки формы обратной связи"""
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print("\n=== ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (CBV) ===")
        print(f"Имя: {name} | Email: {email} | Сообщение: {message}\n")

        context = self.get_context_data()
        context["success"] = True
        return self.render_to_response(context)

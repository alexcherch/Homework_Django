from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Category, ContactInfo, Product


def home(request):
    """Контроллер для отображения главной страницы с пагинацией"""
    products_list = Product.objects.all().order_by("id")

    paginator = Paginator(products_list, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "catalog/home.html", context)


def contacts(request):
    """Контроллер для отображения страницы с контактами"""
    context = {"success": False}

    contact_data = ContactInfo.objects.first()
    context["contact_data"] = contact_data

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print("\n=== ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (DJANGO) ===")
        print(f"Имя: {name} | Email: {email} | Сообщение: {message}\n")

        context["success"] = True

    return render(request, "catalog/contacts.html", context)


def product_detail(request, pk):
    """Контроллер для отображения детальной информации о конкретном товаре"""
    product = get_object_or_404(Product, pk=pk)

    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)


def product_create(request):
    """Контроллер для создания нового товара через форму"""
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        category = get_object_or_404(Category, pk=category_id)

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image,
        )
        return redirect("catalog:home")

    categories = Category.objects.all()
    return render(request, "catalog/product_form.html", {"categories": categories})

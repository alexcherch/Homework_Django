from django.shortcuts import get_object_or_404, render

from catalog.models import ContactInfo, Product


def home(request):
    """Контроллер для отображения главной страницы"""
    products = Product.objects.all()

    context = {"products": products}
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

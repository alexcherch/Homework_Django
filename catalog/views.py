from django.shortcuts import render

from catalog.models import ContactInfo, Product


def home(request):
    """Контроллер для отображения главной страницы"""
    latest_products = Product.objects.all().order_by("-id")[:5]

    print("\n=== ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ ===")
    for product in latest_products:
        print(f"ID: {product.id} | {product.name} | Цена: {product.price}")
    print("========================================\n")

    return render(request, "catalog/home.html")


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

from django.shortcuts import render


def home(request):
    """Контроллер для отображения главной страницы"""
    return render(request, "catalog/home.html")


def contacts(request):
    """Контроллер для отображения страницы с контактами и обработки формы"""
    context = {"success": False}

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print("\n=== ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (DJANGO) ===")
        print(f"Имя: {name}")
        print(f"Email: {email}")
        print(f"Сообщение: {message}")
        print("==========================================\n")

        context["success"] = True

    return render(request, "catalog/contacts.html", context)

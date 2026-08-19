from django.shortcuts import render


def home(request):
    """Контроллер для отображения главной страницы"""
    return render(request, "catalog/home.html")


def contacts(request):
    """Контроллер для отображения страницы с контактами"""
    return render(request, "catalog/contacts.html")

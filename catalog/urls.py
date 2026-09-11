from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsTemplateView, ProductCreateView, ProductDetailView, ProductListView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
]

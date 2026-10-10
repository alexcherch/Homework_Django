from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (CategoryProductsView, ContactsTemplateView, ProductCreateView, ProductDeleteView,
                           ProductDetailView, ProductListView, ProductUnpublishView, ProductUpdateView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("categories/<int:pk>/", CategoryProductsView.as_view(), name="category_products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/unpublish/", ProductUnpublishView.as_view(), name="product_unpublish"),
]

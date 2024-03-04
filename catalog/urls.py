from django.urls import path

from catalog.views import contacts, product_list, product_detail

urlpatterns = [
    path('', product_list),
    path('contacts/', contacts),
    path('products/<int:pk>/', product_detail),
]

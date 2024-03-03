from django.urls import path

from catalog.views import index, contacts, product_list

urlpatterns = [
    path('', product_list),
    path('contacts/', contacts),
    path('products/<int:pk>/', product_list),
]

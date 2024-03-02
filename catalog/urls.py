from django.urls import path

from catalog.views import index, contacts, product_detail

urlpatterns = [
    path('', index),
    path('contacts/', contacts),
    path('products/', product_detail),
]

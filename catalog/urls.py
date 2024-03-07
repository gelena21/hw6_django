from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.views import (ProductUpdateView,
                           ProductDetailView, ProductCreateView,
                           ProductDeleteView, contacts, ProductView)

app_name = 'catalog'

urlpatterns = [
                  path('', ProductView.as_view(),
                       name='index'),
                  path('contacts/', contacts,
                       name='contacts'),
                  path('view/<int:pk>', ProductDetailView.as_view(),
                       name='view'),
                  path('create/', ProductCreateView.as_view(),
                       name='create_product'),
                  path('update/<int:pk>', ProductUpdateView.as_view(),
                       name='update_product'),
                  path('delete/<int:pk>', ProductDeleteView.as_view(),
                       name='delete_product'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

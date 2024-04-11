from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import never_cache, cache_page

from catalog.views import (ProductUpdateView,
                           ProductDetailView, ProductCreateView,
                           ProductDeleteView, contacts, ProductView, categories,
                           category_products)

app_name = 'catalog'

urlpatterns = [
                  path('', ProductView.as_view(),
                       name='index'),
                  path('contacts/', contacts,
                       name='contacts'),
                  path('view/<int:pk>', cache_page(60)(ProductDetailView.as_view()),
                       name='view'),
                  path('create/', never_cache(ProductCreateView.as_view()),
                       name='create_product'),
                  path('update/<int:pk>', ProductUpdateView.as_view(),
                       name='update_product'),
                  path('delete/<int:pk>', ProductDeleteView.as_view(),
                       name='delete_product'),
                  path('categories/', categories, name="categories"),
                  path('<int:pk>/products', category_products, name='category_products'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

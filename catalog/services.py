from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_categories_cash():

    if settings.CASH_ENABLED:
        key = f'categories_list'
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = Category.objects.all()
            cache.set(key, categories_list, 60)
    else:
        categories_list = Category.objects.all()

    return categories_list

import random

from django.core.management import BaseCommand

from catalog.models import Category, Product

class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = []
        for i in range(5):
            category_list.append(
                Category(
                    name=f"Category#{i+1}",
                    description=f"this is another catecory #{i+1}"
                )
            )

        Category.objects.bulk_create(category_list)

        category_id_list = list(Category.objects.all().values_list('id', flat=True))
        max_id = max(category_id_list)
        min_id = min(category_id_list)

        product_list = []
        for i in range(50):
            product_list.append(
                Product(
                    name=f"Product#{i}",
                    description=f"this is description for product #{i}",
                    category_id=random.randint(max_id, min_id),
                    price=random.random() * 1000
                )
            )

        Product.objects.bulk_create(product_list)

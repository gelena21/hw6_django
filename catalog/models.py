from django.db import models

from config import settings

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Наименование категории')
    category_description = models.TextField(max_length=200, verbose_name='Описание категории')

    def __str__(self):
        return f'{self.category_name} {self.category_description}'

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=200, verbose_name='Описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="автор")

    def __str__(self):
        return f'{self.product_name} {self.description} {self.category}'

    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Товары")


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name="Product")
    number = models.IntegerField(verbose_name='номер версии')
    nomination = models.CharField(max_length=50, verbose_name='название')
    is_current = models.BooleanField(default=True, verbose_name='текущая')

    def __str__(self):
        return f'{self.number} ({self.nomination})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
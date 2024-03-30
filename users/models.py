from django.contrib.auth.models import AbstractUser
from django.db import models
from catalog.models import NULLABLE


class User(AbstractUser):
    DoesNotExist = None
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/',
                               verbose_name='аватар', **NULLABLE)
    phone_number = models.CharField(max_length=35,
                                    verbose_name="номер телефона", **NULLABLE)
    country = models.CharField(max_length=255,
                               verbose_name="страна", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователu'

    def __str__(self):
        return f'{self.email} {self.first_name}'

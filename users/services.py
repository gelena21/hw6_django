import random
import string

from django.conf import settings
from django.core.mail import send_mail


def generating_keys(symbols):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=symbols))


def send_registration_mail(obj, site):
    send_mail(
        subject='Регистрация',
        message=f"Вот ваш ключ: {obj.auth_token}\nФорму ввода можно найти по ссылке: {site}/users/verification",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[obj.email],
    )


def send_password_mail(obj, password):
    send_mail(
        subject="Смена пароля",
        message=f'Ваш новый пароль: {password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[obj.email],
    )

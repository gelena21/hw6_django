from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.conf import settings
from users.forms import UserForm, UserForgotPasswordForm
from users.models import User


# Create your views here.

class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    """Представление регистрации на сайте с формой регистрации"""
    model = User
    form_class = UserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email',
                                      kwargs={'uidb64': uid, 'token': token})
        current_site = self.request.get_host()
        send_mail(
            subject='Подтвердите свой электронный адрес',
            message=f'Пожалуйста, перейдите по следующей ссылке, '
                    f'чтобы подтвердить свой адрес электронной '
                    f'почты: http://{current_site}{activation_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if (user is not None and default_token_generator.check_token(user,
                                                                     token)):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
     сброс пароля
     """

    form_class = UserForgotPasswordForm
    template_name = "users/user_password_reset.html"
    success_url = reverse_lazy("catalog:index")
    success_message = (
        "инструкция по" 
        "восстановлению пароля отправлена на ваш email"
    )
    subject_template_name = "users/password_subject_reset_mail.html"
    email_template_name = "users/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserSetNewPasswordForm:
    pass


class UserPasswordResetConfirmView(SuccessMessageMixin,
                                   PasswordResetConfirmView):
    """Представление установки нового пароля"""

    form_class = UserSetNewPasswordForm
    template_name = "users/user_password_set_new.html"
    success_url = reverse_lazy("catalog:index")
    success_message = ("Пароль успешно изменен. "
                       "Можете авторизоваться на сайте.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context

from django.urls import path
from django.views.decorators.cache import never_cache

from users.apps import UsersConfig
from users.views import RegisterView, UserForgotPasswordView, EmailConfirmationSentView, UserConfirmEmailView, \
    EmailConfirmedView, EmailConfirmationFailedView, UserPasswordResetConfirmView, LoginView, LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('', never_cache(LoginView.as_view()), name='login'),
    path('logout/', never_cache(LogoutView.as_view()), name='logout'),
    path('register/', never_cache(RegisterView.as_view()), name='register'),
    path("password-reset/",never_cache( UserForgotPasswordView.as_view()),
         name="password_reset"),
    path(
        "set-new-password/<uidb64>/<token>/",
        never_cache(UserPasswordResetConfirmView.as_view()),
        name="password_reset_confirm",
    ),
    path(
        "email-confirmation-sent/",
        never_cache(EmailConfirmationSentView.as_view()),
        name="email_confirmation_sent",
    ),
    path(
        "confirm-email/<str:uidb64>/<str:token>/",
        never_cache(UserConfirmEmailView.as_view()),
        name="confirm_email",
    ),
    path("email-confirmed/",
         never_cache(EmailConfirmedView.as_view()),
         name="email_confirmed"),
    path(
        "confirm-email-failed/",
        never_cache(EmailConfirmationFailedView.as_view()),
        name="email_confirmation_failed",
    ),
]

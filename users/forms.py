from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from users.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserForgotPasswordForm(PasswordResetForm):
    """
    восстановление пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )

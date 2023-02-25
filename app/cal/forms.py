from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-input'})),
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-input'})),
    password1 = forms.CharField(label='Пароль', max_length=150,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'})),
    password2 = forms.CharField(label='Подтверждение пароля', max_length=150,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'})),

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-input'})),
    password1 = forms.CharField(label='Пароль', max_length=150,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'})),
    class Meta:
        model = User
        fields = ('username', 'password1')
    # username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    # password = forms.CharField(
    #     label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    # )


    # def __init__(self, request=None, *args, **kwargs):
    #     """
    #     The 'request' parameter is set for custom auth use by subclasses.
    #     The form data comes in via the standard 'data' kwarg.
    #     """
    #     self.request = request
    #     self.user_cache = None
    #     super().__init__(*args, **kwargs)

    #     # Set the max length and label for the "username" field.
    #     self.username_field = UserModel._meta.get_field(
    #         UserModel.USERNAME_FIELD)
    #     username_max_length = self.username_field.max_length or 254
    #     self.fields["username"].max_length = username_max_length
    #     self.fields["username"].widget.attrs["maxlength"] = username_max_length
    #     if self.fields["username"].label is None:
    #         self.fields["username"].label = capfirst(
    #             self.username_field.verbose_name)

    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

    #     if username is not None and password:
    #         self.user_cache = authenticate(
    #             self.request, username=username, password=password
    #         )
    #         if self.user_cache is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(self.user_cache)

    #     return self.cleaned_data

    # def confirm_login_allowed(self, user):
    #     """
    #     Controls whether the given User may log in. This is a policy setting,
    #     independent of end-user authentication. This default behavior is to
    #     allow login by active users, and reject login by inactive users.

    #     If the given user cannot log in, this method should raise a
    #     ``ValidationError``.

    #     If the given user may log in, this method should return None.
    #     """
    #     if not user.is_active:
    #         raise ValidationError(
    #             self.error_messages["inactive"],
    #             code="inactive",
    #         )

    # def get_user(self):
    #     return self.user_cache

    # def get_invalid_login_error(self):
    #     return ValidationError(
    #         self.error_messages["invalid_login"],
    #         code="invalid_login",
    #         params={"username": self.username_field.verbose_name},
    #     )

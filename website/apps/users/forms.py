import unicodedata

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from .models import User, OK_STATUS


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'login', 'social_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("Podany email już jest użyty.")

        return email

    def clean_login(self):
        login = self.cleaned_data.get('login')
        qs = User.objects.filter(login=login)

        if qs.exists():
            raise forms.ValidationError("Podany login jest już zajęty")

        return login

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Hasła się nie zgadzają")

        if len(password2) < 4:
            raise forms.ValidationError("Hasło musi mieć co najmniej 4 znaków")

        return password2        


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'login', 'social_id')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("Podany email już jest użyty.")

        return email

    def clean_login(self):
        login = self.cleaned_data.get('login')
        qs = User.objects.filter(login=login)

        if qs.exists():
            raise forms.ValidationError("Podany login jest już zajęty")

        return login

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła się nie zgadzają")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class UserAdminChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'login', 'social_id')


def _unicode_ci_compare(s1, s2):
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = get_user_model()._default_manager.filter(**{
            '%s__iexact' % 'email': email,
            'status': OK_STATUS,
        })

        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, 'email'))
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )

        return password2

from django import forms

from .models import User


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

from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    # форма, которая будет использоваться для авторизации пользователя
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Reapeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        def clean_password2(self):
            # проверяем, совпадают ли оба пароля
            cd = self.clean_password2
            if cd['password'] != cd['password2']:
                raise forms.ValidationError("Passwords don't match.")
            return cd['password2']


class UserEditForm(forms.ModelForm):
    # UserEditForm – позволит пользователям менять имя, фамилию, e-mail
    # (поля встроенной в Django модели);
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    # ProfileEditForm – позволит модифицировать дополнительные сведения,
    # которые мы сохраняем в модели Profile (дату рождения и аватар).
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from catalog.forms import StyleMixin
from .models import CustomUser


# Форма регистрации
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False)
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите ник'
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Введите почту'
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите ваш номер телефона',
            }
        )

        self.fields['password1'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите ваш пароль'
            }
        )

        self.fields['password2'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Повторно введите ваш пароль'
            }
        )

        self.fields['country'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите страну'
            }
        )
        self.fields['avatar'].widget.attrs.update(
            {
                'class': 'form-control',
            }
        )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'country', 'avatar', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры.')
        return phone_number


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username","email", "phone_number", "country", "avatar"]
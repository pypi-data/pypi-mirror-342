from django import forms
from django.contrib.auth.models import User
from .models import Request
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate
from django.utils import timezone

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')
    full_name = forms.CharField(max_length=255, required=True, label='ФИО')
    phone = forms.CharField(
        max_length=20,
        required=True,
        label='Телефон',
        widget=forms.TextInput(attrs={
            'placeholder': '+7(___)___-__-__',  # Плейсхолдер с маской
            'data-mask': '+7(000)000-00-00',    # Маска для ввода
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',  # Разрешаем только цифры
        }),
    )
    email = forms.EmailField(required=True, label='Электронная почта')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Этот логин уже занят.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 6:
            raise ValidationError("Пароль должен содержать минимум 6 символов.")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        
        if not re.search(r'\d', password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Пароль должен содержать хотя бы один специальный символ.")
        
        return password

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[А-Яа-яЁё\s]+$', full_name):
            raise ValidationError("ФИО должно содержать только кириллицу и пробелы.")
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$', phone):
            raise ValidationError("Телефон должен быть в формате +7(XXX)-XXX-XX-XX.")
        return phone

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль.")
            
class RequestForm(forms.ModelForm):
    other_service = forms.BooleanField(required=False, label='Иная услуга')
    other_service_description = forms.CharField(required=False, label='Описание иной услуги')

    class Meta:
        model = Request
        fields = ['service', 'address', 'contact_number', 'date_time', 'payment_type', 'other_service', 'other_service_description']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # Используем тип datetime-local для выбора даты и времени
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M'),  # Устанавливаем минимальную дату на текущее время
            }),
            'contact_number': forms.TextInput(attrs={
                'placeholder': '+7(___)___-__-__',  # Плейсхолдер с маской
                'data-mask': '+7(000)000-00-00',  # Маска для ввода
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")',  # Разрешаем только цифры
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        other_service = cleaned_data.get('other_service')
        other_service_description = cleaned_data.get('other_service_description')

        if other_service and not other_service_description:
            raise forms.ValidationError("Пожалуйста, укажите описание иной услуги.")

        return cleaned_data

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not re.match(r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$', contact_number):
            raise forms.ValidationError("Телефон должен быть в формате +7(XXX)-XXX-XX-XX.")
        return contact_number
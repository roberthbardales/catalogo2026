from django import forms
from django.core.validators import RegexValidator

from .models import User


phone_validator = RegexValidator(
    regex=r'^[\d\s\-\+\(\)]{7,20}$',
    message='Ingresa un número de teléfono válido.'
)


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombres', max_length=50)
    last_name = forms.CharField(label='Apellidos', max_length=50)
    occupation = forms.ChoiceField(label='Rol', choices=User.OCCUPATION_CHOICES, required=False)
    gender = forms.ChoiceField(label='Género', choices=User.GENDER_CHOICES)
    phone = forms.CharField(label='Celular', max_length=20, required=False, validators=[phone_validator])
    date_birth = forms.DateField(
        label='Fecha de nacimiento',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    )
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.is_admin_context = kwargs.pop('is_admin_context', False)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        if not self.is_admin_context:
            self.fields.pop('occupation')
        else:
            self.fields['occupation'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return phone
        normalized_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        return normalized_phone


class UserUpdateForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombres', max_length=50)
    last_name = forms.CharField(label='Apellidos', max_length=50)
    occupation = forms.ChoiceField(label='Rol', choices=User.OCCUPATION_CHOICES, required=False)
    gender = forms.ChoiceField(label='Género', choices=User.GENDER_CHOICES)
    phone = forms.CharField(label='Celular', max_length=20, required=False, validators=[phone_validator])
    date_birth = forms.DateField(
        label='Fecha de nacimiento',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    )
    def __init__(self, *args, **kwargs):
        self.is_admin_context = kwargs.pop('is_admin_context', False)
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        if not self.is_admin_context:
            self.fields.pop('occupation')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email

        qs = User.objects.filter(email__iexact=email)
        if self.user_instance is not None:
            qs = qs.exclude(pk=self.user_instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe otro usuario con ese correo electrónico.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return phone
        normalized_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        return normalized_phone


class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data


class UpdatePasswordForm(forms.Form):
    current_password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput)
    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('La nueva contraseña y su confirmación no coinciden.')

        return cleaned_data

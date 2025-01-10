from django import forms
from .models import Grupo, Producto, Venta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'fecha_caducidad', 'categoria', 'proveedor']

class GrupoForm(forms.ModelForm):
    medicamentos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Grupo
        fields = ['nombre', 'categoria', 'color', 'medicamentos']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

class EntregaElementosForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'destinatario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'destinatario': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rut = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'rut', 'fecha_nacimiento', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
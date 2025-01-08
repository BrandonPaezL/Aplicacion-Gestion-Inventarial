# forms.py
from django import forms
from .models import Grupo, Producto, Venta

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
        fields = ['producto', 'cantidad', 'destinatario']  # Incluir el nuevo campo
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'destinatario': forms.TextInput(attrs={'class': 'form-control'}),  # Widget para el nuevo campo
        }
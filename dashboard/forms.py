# forms.py
from django import forms
from .models import Grupo, Producto

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
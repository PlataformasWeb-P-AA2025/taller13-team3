from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

from departamentos.models import Edificio, Departamento


class EdificioForm(ModelForm):
    class Meta:
        model = Edificio
        fields = ['nombre', 'direccion', 'ciudad', 'tipo']
        labels = {
            'nombre': _('Ingrese el nombre del edificio por favor'),
            'direccion': _('Ingrese la dirección por favor'),
            'ciudad': _('Ingrese la ciudad por favor'),
            'tipo': _('Seleccione el tipo de edificio'),
        }

    def clean_nombre(self):
        valor = self.cleaned_data['nombre']
        if len(valor) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres")
        return valor

    def clean_direccion(self):
        valor = self.cleaned_data['direccion']
        if len(valor) < 5:
            raise forms.ValidationError("Ingrese una dirección válida (mínimo 5 caracteres)")
        return valor

    def clean_ciudad(self):
        valor = self.cleaned_data['ciudad']
        if len(valor) < 3:
            raise forms.ValidationError("Ingrese una ciudad válida")
        return valor


class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        fields = ['nombre_propietario', 'costo', 'numero_cuartos', 'edificio']


class DepartamentoEdificioForm(ModelForm):
    def __init__(self, edificio, *args, **kwargs):
        super(DepartamentoEdificioForm, self).__init__(*args, **kwargs)
        self.initial['edificio'] = edificio
        self.fields["edificio"].widget = forms.widgets.HiddenInput()

    class Meta:
        model = Departamento
        fields = ['nombre_propietario', 'costo', 'numero_cuartos', 'edificio']

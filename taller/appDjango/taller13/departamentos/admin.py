from django.contrib import admin
from departamentos.models import Edificio, Departamento

# Register your models here.

# Admin para Edificio
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'ciudad', 'tipo')
    search_fields = ('nombre', 'ciudad')

admin.site.register(Edificio, EdificioAdmin)

# Admin para Departamento
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre_propietario', 'costo', 'numero_cuartos', 'edificio')
    raw_id_fields = ('edificio',)  # Para seleccionar el edificio mediante búsqueda

admin.site.register(Departamento, DepartamentoAdmin)

from django.db import models

# Create your models here.

class Edificio(models.Model):
    edificio_opciones = (
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial')
    )

    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=30)
    tipo = models.CharField(max_length=20, choices=edificio_opciones)

    def __str__(self):
        return f"{self.nombre} - {self.tipo} ({self.ciudad})"


class Departamento(models.Model):
    nombre_propietario = models.CharField(max_length=100)
    costo = models.FloatField()
    numero_cuartos = models.IntegerField()
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="departamentos")

    def __str__(self):
        return f"{self.nombre_propietario} - ${self.costo} - {self.numero_cuartos} cuartos"


from django.db import models
from django.conf import settings

class GestorRegistrarVentaEntradas(models.Model):
    cantidadEntradas = models.IntegerField()
    cantMaximaVisitantes = models.IntegerField()
    cantVisitantesActuales = models.IntegerField()
    ultimoNroEntrada = models.IntegerField()
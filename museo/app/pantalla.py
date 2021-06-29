from .models import *

class PantallaSala(models.Model):
    cantVisitantes = models.IntegerField(null=False)

    def __str__(self):
        return '{}'.format(self.cantVisitantes)

    def actualizarCantVisitantes(self, cantidad):
        self.cantVisitantes = cantidad
        return self.cantVisitantes

class PantallaEntrada(models.Model):
    cantVisitantes = models.IntegerField(null=False)

    def __str__(self):
        return '{}'.format(self.cantVisitantes)

    def actualizarCantVisitantes(self, cantidad):
        self.cantVisitantes = cantidad
        return self.cantVisitantes
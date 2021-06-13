from django.db import models

# Create your models here.

class TipoVisita(models.Model):
    nombre = models.CharField(null=False, max_length=20)

    def __str__(self):
        return 'Tipo de Visita: {}'.format(self.nombre)

class TipoDeEntrada(models.Model):
    nombre = models.CharField(null=False, max_length=20)

    def __str__(self):
        return 'Tipo de Entrada: {}'.format(self.nombre)

class Tarifa(models.Model):
    fechaFinVigencia = models.DateTimeField()
    fechaInicioVigencia = models.DateTimeField()
    monto = models.FloatField()
    montoAdicionalGuia = models.FloatField()

    def __str__(self):
        return 'Monto: {} - Monto con Guia {}'.format(self.monto, self.montoAdicionalGuia)

class HorarioSede(models.Model):
    horaApertura = models.TimeField()
    horaCierre = models.TimeField()

    def __str__(self):
        return 'Hora Apertura {} - Hora Cierre {}'.format(self.horaApertura, self.horaCierre)

class Obra(models.Model):
    alto = models.FloatField()
    ancho = models.FloatField()
    codigoSensor = models.CharField(max_length=20)
    descripcion = models.TextField()
    

class Sede(models.Model):
    cantMaximaVisitantes = models.IntegerField(null=False)
    cantMaxPorGuia = models.IntegerField(null=False)
    nombre = models.CharField(null=False, max_length=50)

    def __str__(self):
        return 'Sede: {}'.format(self.nombre)

    
    @classmethod
    def getSedes(cls):
        #queryset = cls.objects.raw('SELECT * FROM app_Sede')
        # can use the below method also
        # queryset = self.__class__.objects.all()   
        queryset = Sede.objects.all()
        return queryset

class Empleado(models.Model):
    apellido = models.CharField(null=False, max_length=20)
    codigoValidacion = models.CharField(max_length=20)
    cuit = models.IntegerField()
    dni = models.IntegerField(null=False)
    domicilio = models.CharField(max_length=80)
    fechaIngreso = models.DateTimeField()
    fechaNacimiento = models.DateTimeField()
    mail = models.EmailField()
    nombre = models.CharField(null=False, max_length=20)
    sexo = models.CharField(max_length=10)
    telefono = models.IntegerField()

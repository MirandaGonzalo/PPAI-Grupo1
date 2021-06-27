from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.

class Sede(models.Model):
    cantMaximaVisitantes = models.IntegerField(null=False)
    cantMaxPorGuia = models.IntegerField(null=False)
    nombre = models.CharField(null=False, max_length=50)

    def __str__(self):
        return '{}'.format(self.nombre)
    
    @classmethod
    def getSedes(cls):
        queryset = Sede.objects.all()
        return queryset

    def getExposiciones(sede):
        return sede.exposicion_set.all()

    def getCantMaximaVisitantes(sede):
        return sede.cantMaximaVisitantes

    def getDatosTarifasVigentes(sede):
        tarifas =  sede.tarifa_set.all()
        tarifasVigentes = []
        for a in tarifas:
            resultado = Tarifa.esVigente(a)
            if (resultado):
                tarifasVigentes.append(a)
        #return tarifasVigentes
        return tarifas

class TipoVisita(models.Model):
    nombre = models.CharField(null=False, max_length=20)

    def mostrarNombre(self):
        return self.nombre

    def __str__(self):
        return 'Tipo de Visita: {}'.format(self.nombre)

class TipoEntrada(models.Model):
    nombre = models.CharField(null=False, max_length=20)

    def mostrarNombre(self):
        return self.nombre

    def __str__(self):
        return 'Tipo de Entrada: {}'.format(self.nombre)

class Tarifa(models.Model):
    fechaFinVigencia = models.DateTimeField()
    fechaInicioVigencia = models.DateTimeField()
    monto = models.FloatField()
    montoAdicionalGuia = models.FloatField()
    tipoVisita = models.ForeignKey(TipoVisita, on_delete=models.CASCADE)
    tipoEntrada = models.ForeignKey(TipoEntrada, on_delete=models.CASCADE) 
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    
    def conocerTipoEntrada(self):
        return self.tipoEntrada.mostrarNombre()

    def conocerTipoVisita(self):
        return self.tipoVisita.mostrarNombre()

    def getMonto(self):
        return self.monto

    def getMontoAdicionalGuia(self):
        return self.montoAdicionalGuia
    
    def esVigente(tarifa):        
        ahora = datetime.now()
        fechafinVigencia = tarifa.fechaFinVigencia
        x = datetime(fechafinVigencia.year,fechafinVigencia.month,fechafinVigencia.day,fechafinVigencia.hour,fechafinVigencia.minute,fechafinVigencia.second)        
        if (x > ahora):
            return True
        return False


    @classmethod
    def getTarifas(cls):
        queryset = Tarifa.objects.all()
        return queryset

    def __str__(self):
        return 'Monto: {} - Monto con Guia {}'.format(self.monto, self.montoAdicionalGuia)

class Entrada(models.Model):
    fechaVenta = models.DateTimeField()
    horaVenta = models.TimeField()
    monto = models.FloatField()
    numero = models.AutoField(primary_key=True)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    def esVigente(self):
        """
        falta hacer
        """
        return True

    def getFechahora(self):
        return self.fechaVenta, self.horaVenta

    def getNumero(self):
        return self.numero

class HorarioSede(models.Model):
    horaApertura = models.TimeField()
    horaCierre = models.TimeField()

    def __str__(self):
        return 'Hora Apertura {} - Hora Cierre {}'.format(self.horaApertura, self.horaCierre)

class Exposicion(models.Model):
    fechaFin = models.DateTimeField()
    fechaFinReplanificada = models.DateTimeField()
    fechaIncio = models.DateTimeField()
    fechaInicioReplanificada = models.DateTimeField()
    horaApertura = models.TimeField()
    horaCierre = models.TimeField()
    nombre = models.CharField(null=False,max_length=20)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)

    def esVigente(self):        
        return True

    def calcularDuracionResumidaXObra(self):
        detalles = DetalleExposicion.objects.filter(exposicion=self)
        total = 0
        for a in detalles:
            obra = Obra.objects.get(id=a.obra.id)
            total += obra.duracionResumida
        return total

class Obra(models.Model):
    alto = models.FloatField()
    ancho = models.FloatField()
    codigoSensor = models.CharField(max_length=20)
    descripcion = models.TextField()
    duracionExtendida = models.FloatField()
    duracionResumida = models.FloatField()
    fechaCreacion = models.DateTimeField()
    fechaPrimerIngreso = models.DateTimeField()
    nombreObra = models.CharField(max_length=20)
    peso = models.FloatField()
    valuacion = models.FloatField()

    def getDuracionResumida(self):
        return self.duracionResumida

class DetalleExposicion(models.Model):
    lugarAsignado = models.CharField(max_length=20)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    exposicion = models.ForeignKey(Exposicion, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.obra.nombreObra, self.lugarAsignado)

class Empleado(models.Model):
    nombre = models.CharField(null=False, max_length=20)
    apellido = models.CharField(null=False, max_length=20)
    codigoValidacion = models.CharField(max_length=20)
    cuit = models.IntegerField()
    dni = models.IntegerField(null=False)
    domicilio = models.CharField(max_length=80)
    fechaIngreso = models.DateTimeField()
    fechaNacimiento = models.DateTimeField()
    mail = models.EmailField()
    sexo = models.CharField(max_length=10)
    telefono = models.IntegerField()
    sede = models.OneToOneField(
        Sede,
        on_delete=models.CASCADE,
        null = False,
        related_name = 'Sedes'
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.DO_NOTHING, null=True)
        
    def getNombreSede(self):
        return self.sede.cantMaxPorGuia

    def getEmpleadoFromUsuario(usuario):
        empleado = Empleado.objects.get(user=usuario)
        return empleado

    def __str__(self):
        return '{} {} - Sede: {}'.format(self.apellido, self.nombre, Empleado.getNombreSede(self))
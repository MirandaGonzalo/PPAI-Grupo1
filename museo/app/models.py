from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import date, time 
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
        tarifas = sede.tarifa_set.all()
        tarifasVigentes = []
        for a in tarifas:
            resultado = a.esVigente()
            if (resultado):
                tarifasVigentes.append(a)
        #return tarifasVigentes
        return tarifas

    def calcularDuracionVisitaCompleta(sede):
        exposicionesSede = sede.exposicion_set.all()
        duracionVisitaTotal = 0
        if (exposicionesSede.count() > 0):
            for a in exposicionesSede:
                es_vigente = Exposicion.esVigente(a)
                if (es_vigente):
                    duracionVisitaTotal += Exposicion.calcularDuracionResumidaXObra(a)
        return duracionVisitaTotal

    def calcularCantEntradasReservas(sede,fechaHoraActual):
        reservas = sede.reservavisita_set.all()
        cantAlumnosConfirmados = 0
        if (reservas.count() > 0):
            for a in reservas:
                vigencia = ReservaVisita.esVigente(a,fechaHoraActual)
                if (vigencia):
                    cantAlumnosConfirmados += a.getCantAlumnosConfirmada()
        return cantAlumnosConfirmados

    def calcularCantVisitantesActuales(sede,fechaHoraActual):
        entradasReserva = Sede.calcularCantEntradasReservas(sede,fechaHoraActual)
        entradasParticuales = Sede.calcularCantEntradasParticulares(sede,fechaHoraActual)
        return (entradasReserva + entradasParticuales)

    def calcularCantEntradasParticulares(sede,fechaHoraActual):
        return Entrada.estaEnMuseo(sede,fechaHoraActual)

class ReservaVisita(models.Model):
    cantAlumnos = models.IntegerField(null=False)
    cantAlumnosConfirmada = models.IntegerField(null=False)
    duracionEstimada = models.IntegerField(null=False)
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True)
    fechaHoraReserva = models.DateTimeField(null=False)
    horaFinReal = models.TimeField()
    horaInicioReal = models.TimeField()
    numeroReserva = models.IntegerField(null=False)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    def esVigente(reserva, fechaHoraActual):
        fechaReservaS = reserva.fechaHoraReserva
        fechaReserva = datetime(fechaReservaS.year,fechaReservaS.month,fechaReservaS.day)
        fechaActualSistema = datetime(fechaHoraActual.year,fechaHoraActual.month,fechaHoraActual.day)        
        horaActualSistema = time(fechaHoraActual.hour,fechaHoraActual.minute,fechaHoraActual.second)
        horaInicioRes = reserva.horaInicioReal
        horaFinRes = reserva.horaFinReal
        horaInicioR = time(horaInicioRes.hour, horaInicioRes.minute, horaInicioRes.second)
        if (fechaReserva == fechaActualSistema):
            if (horaInicioRes is not None and horaFinRes is None):
                if (horaInicioR < horaActualSistema):
                    return True
        return False
    
    def getCantAlumnosConfirmada(self):
        return self.cantAlumnosConfirmada

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
    fechaVenta = models.DateTimeField(auto_now_add=True)
    horaVenta = models.TimeField(null=False)
    monto = models.FloatField(null=False)
    numero = models.IntegerField(primary_key=True)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = ['numero']

    def __str__(self):
        return '{} - {}'.format(self.sede.nombre, self.numero)

    def estaEnMuseo(sede,fechaHoraActual):
        return Entrada.objects.filter(sede__id=sede.id,fechaVenta__year=fechaHoraActual.year, fechaVenta__month=fechaHoraActual.month,fechaVenta__day=fechaHoraActual.day).count()

    def getFechahora(self):
        return self.fechaVenta, self.horaVenta

    def getNumero():
        return Entrada.objects.latest()


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

    def esVigente(exposicion):        
        ahora = datetime.now()
        fechaFin = exposicion.fechaFin
        if (exposicion.fechaFinReplanificada is None):
            fechaFinExposicion = datetime(fechaFin.year,fechaFin.month,fechaFin.day,fechaFin.hour,fechaFin.minute,fechaFin.second)        
            if (fechaFinExposicion > ahora):
                return True
            return False
        else:
            fechaRep = exposicion.fechaFinReplanificada
            fechaFinRep = datetime(fechaRep.year,fechaRep.month,fechaRep.day,fechaRep.hour,fechaRep.minute,fechaRep.second)
            print (fechaFinRep)
            if (fechaFinRep > ahora):
                return True
        return False

    def calcularDuracionResumidaXObra(exposicion):
        detalles = exposicion.detalleexposicion_set.all()
        total = 0
        for a in detalles:
            obra = Obra.objects.get(id=a.obra.id)
            total += Obra.getDuracionResumida(obra)
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
        
    def getSede(self):
        return self.sede

    def conocerEmpleado(usuario):
        empleado = Empleado.objects.get(user=usuario)
        return empleado


    def __str__(self):
        return '{} {} - Sede: {}'.format(self.apellido, self.nombre, Empleado.getNombreSede(self))
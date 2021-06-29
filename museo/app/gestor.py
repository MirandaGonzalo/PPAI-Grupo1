from .models import *
from .pantalla import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


class GestorRegistrarVentaEntradas(models.Model):
    cantidadEntradas = models.IntegerField()
    cantMaximaVisitantes = models.IntegerField()
    cantVisitantesActuales = models.IntegerField()
    ultimoNroEntrada = models.IntegerField()

    def buscarSedeActual(request):        
        empleado = Empleado.conocerEmpleado(request.user)
        sede = empleado.getSede()
        return sede

    def calcularDuracionVisitaCompleta(sede):
        duracion = sede.calcularDuracionVisitaCompleta()
        return duracion

    def buscarTarifasDeSede(sede):
        tarifasVigentes = sede.getDatosTarifasVigentes()
        return tarifasVigentes

    def obtenerFechaHoraActual():
        return datetime.now()

    def validarCantEntradas(sede, cantidad):
        maxVisitantes = sede.getCantMaximaVisitantes()
        fechaHoraActual = GestorRegistrarVentaEntradas.obtenerFechaHoraActual()        
        return (Sede.calcularCantVisitantesActuales(sede,fechaHoraActual) + cantidad <= maxVisitantes)
    
    def calcularTotalTarifas(cantidad, monto):        
        return (float(cantidad) * float(monto))

    def crearEntrada(fechaVenta, horaVenta, monto, numero,sede,tarifa):
        entrada = Entrada(fechaVenta=fechaVenta, horaVenta=horaVenta, monto=monto, numero=numero,sede=sede,tarifa=tarifa)
        entrada.save()
        return entrada

    def buscarUltimoNroEntrada():
        ultima_entrada = Entrada.getNumero()
        return ultima_entrada.numero

    def imprimirEntrada(request, entradas,total):
        sede = GestorRegistrarVentaEntradas.buscarSedeActual(request)
        html_string = render_to_string('imprimir.html', {'sede': sede,'entradas':entradas,'total':total})
        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/detalleVenta.pdf')
        fs = FileSystemStorage('/tmp')
        with fs.open('detalleVenta.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="detalleMuseo.pdf"'
            return response

    def actualizarPantallas(cantidad):
        PantallaSala.actualizarCantVisitantes(cantidad)
        PantallaEntrada.actualizarCantVisitantes(cantidad)
        return True
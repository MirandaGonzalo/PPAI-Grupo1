from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.core import serializers
from django.db import transaction
from django.urls import reverse
from django.utils.dateparse import parse_date
from .models import *
from .gestor import *
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from django import forms
from django.contrib import messages
from .scriptBase import *
from weasyprint import HTML


def loginForm(request):
    return render(request, 'login/loginForm.html')

def perfil(request):
    sedeDelEmpleado = GestorRegistrarVentaEntradas.buscarSedeActual(request)
    empleado = Empleado.conocerEmpleado(request.user)
    return render(request, 'perfil.html', {'empleado':empleado,'sedeDelEmpleado':sedeDelEmpleado})

def logOutUser(request):
    logout(request)
    return redirect(loginForm)

def registrarVentaEntrada(request):
    actualSede = GestorRegistrarVentaEntradas.buscarSedeActual(request)
    tarifas = GestorRegistrarVentaEntradas.buscarTarifasDeSede(actualSede)
    return render(request,'registrarVentaEntrada.html',{'tarifas':tarifas})

def calcularDuracionVisita(request):
    data = {
        'duracion' : 0
    }
    if (request.method == 'POST'):
        actualSede = GestorRegistrarVentaEntradas.buscarSedeActual(request)
        duracion = GestorRegistrarVentaEntradas.calcularDuracionVisitaCompleta(actualSede)
        data = {
            'duracion' : duracion
        }
        return JsonResponse(data)
    return JsonResponse(data)
    

def validarCantidadEntradas(request):
    data = {
        'result' : 'Error, la operacion fracasó.',
        'estado': False
    }
    if request.method == 'POST':
        cantidad = request.POST['cantidad']
        cantidadSolicitada = int(cantidad)
        actualSede = GestorRegistrarVentaEntradas.buscarSedeActual(request)
        result = GestorRegistrarVentaEntradas.validarCantEntradas(actualSede,cantidadSolicitada)
        data = {
            'estado': result
        }        
        return JsonResponse(data)
    return JsonResponse(data)

def calcularTotalTarifas(request):
    data = {
        'result' : 'Error, la operacion fracasó.',
        'estado': False
    }
    if request.method == 'POST':        
        cantidad = request.POST['cantidad']
        tarifa = request.POST['tarifa']
        cantidadSolicitada = int(cantidad)
        idTarifa = int(tarifa)
        tarifa = Tarifa.objects.get(id=idTarifa)
        total = GestorRegistrarVentaEntradas.calcularTotalTarifas(cantidadSolicitada, tarifa.monto)
        listaEntradas = []
        for i in range(0,cantidadSolicitada):            
            listaEntradas.append(i+1)
        return render(request, 'detalleVenta.html', {'listaEntradas':listaEntradas, 'total':total,'monto':tarifa.monto })
    return JsonResponse(data)

entradas = []
total = []
def crearEntrada(request):
    data = {
        'result' : 'Error, la operacion fracasó.',
        'estado': False,
        'entradas': ""
    }
    if request.method == 'POST':
        cantidad = request.POST['cantidad']
        tarifa = request.POST['tarifa']
        cantidadSolicitada = int(cantidad)
        idTarifa = int(tarifa)
        tarifaSeleccionada = Tarifa.objects.get(id=idTarifa)
        fechaActual = GestorRegistrarVentaEntradas.obtenerFechaHoraActual()
        fechaVenta = datetime(fechaActual.year, fechaActual.month, fechaActual.day)
        horaVenta = time(fechaActual.hour, fechaActual.minute, fechaActual.second)
        actualSede = GestorRegistrarVentaEntradas.buscarSedeActual(request)
        for i in range(0,cantidadSolicitada):
            numero = (GestorRegistrarVentaEntradas.buscarUltimoNroEntrada() + 1)
            entrada = GestorRegistrarVentaEntradas.crearEntrada(fechaVenta, horaVenta, tarifaSeleccionada.monto, numero,actualSede,tarifaSeleccionada) 
            entradas.append(entrada)
        data = {
            'estado': True
        }
        totalAux = GestorRegistrarVentaEntradas.calcularTotalTarifas(cantidadSolicitada,tarifaSeleccionada.monto )
        total.append(totalAux)        
    return JsonResponse(data)

def imprimirEntrada(request):
    totalF = 0
    for a in total:
        totalF = a
    return GestorRegistrarVentaEntradas.imprimirEntrada(request,entradas,totalF)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('registrarVentaEntrada')
        else:
            messages.error(request,'Los datos ingresados no son correctos.')
            return redirect('loginForm')
    else:
        form = LoginForm()
    return render(request, 'login/loginForm.html', {'form': form})
    
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

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
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from django import forms
from django.contrib import messages
from .scriptBase import *

def landing_page(request):
    return render(request, 'index.html')

def loginForm(request):
    return render(request, 'login/loginForm.html')

def perfil(request):
    sedes = Sede.getSedes()    
    empleado = Empleado.getEmpleadoFromUsuario(request.user)
    sedeDelEmpleado = Sede.objects.get(id=empleado.sede.id)
    tarifas = Sede.getDatosTarifasVigentes(sedeDelEmpleado)    
    return render(request, 'perfil.html', {'empleado':empleado,'sedeDelEmpleado':sedeDelEmpleado})

def logOutUser(request):
    logout(request)
    return redirect(loginForm)

def registrarVentaEntrada(request):
    empleado = Empleado.getEmpleadoFromUsuario(request.user)
    sedeDelEmpleado = Sede.objects.get(id=empleado.sede.id)
    tarifas = Sede.getDatosTarifasVigentes(sedeDelEmpleado)
    return render(request,'registrarVentaEntrada.html',{'tarifas':tarifas})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('perfil')
        else:
            messages.error(request,'Los datos ingresados no son correctos.')
            return redirect('loginForm')
    else:
        form = LoginForm()
    return render(request, 'login/loginForm.html', {'form': form})
    
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

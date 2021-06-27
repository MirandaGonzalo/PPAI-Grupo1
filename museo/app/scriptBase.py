import datetime
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
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from django import forms
from django.contrib import messages

def crearObjetos(request):
    """
    for a in range(10):
        alto = a
        ancho = a
        codigoSensor = "qwert" + str(a)
        descripcion = "descripcion" + str(a)
        duracionExtendida = a * 40
        duracionResumida = a * 20
        fechaCreacion = datetime.today()
        fechaPrimerIngreso = datetime.today()
        nombreObra = "el grito " + str(a)
        peso = a * 10.5
        valuacion = 10
        obra1 = Obra(alto=alto,ancho=ancho,codigoSensor=codigoSensor,descripcion=descripcion,
        duracionExtendida=duracionExtendida,duracionResumida=duracionResumida,fechaCreacion=fechaCreacion,
        fechaPrimerIngreso=fechaPrimerIngreso,nombreObra=nombreObra,peso=peso,valuacion=valuacion)
        obra1.save()
    """
    for a in range(3):
        cantV = a * 100
        cantM = a * 88
        nombre = "Sede " + str(a)
        sede = Sede(cantMaximaVisitantes=cantV, cantMaxPorGuia=cantM, nombre=nombre)
        sede.save()

    return True
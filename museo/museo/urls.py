from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginForm, name='loginForm'),
    path('loginForm/', loginForm, name='loginForm'),
    path('logOutUser/', logOutUser, name='logOutUser'),
    path('login/', login, name='login'),
    path('registrarVentaEntrada/', registrarVentaEntrada, name='registrarVentaEntrada'),
    path('calcularDuracionVisita/', calcularDuracionVisita, name='calcularDuracionVisita'),
    path('validarCantidadEntradas/', validarCantidadEntradas, name='validarCantidadEntradas'),
    path('calcularTotalTarifas/', calcularTotalTarifas, name='calcularTotalTarifas'),
    path('crearEntrada/', crearEntrada, name='crearEntrada'),
    path('imprimirEntrada/', imprimirEntrada, name='imprimirEntrada'),
    path('pantallaSala/', pantallaSala, name='pantallaSala'),
    path('pantallaSede/', pantallaSede, name='pantallaSede'),
    path('actualizarPantallas/', actualizarPantallas, name='actualizarPantallas')
]

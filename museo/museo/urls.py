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
    path('perfil/', perfil, name='perfil')
]
from django.contrib import admin
from .models import *

admin.site.register(Sede)
admin.site.register(Empleado)
admin.site.register(TipoVisita)
admin.site.register(TipoEntrada)
admin.site.register(Tarifa)
admin.site.register(Obra)
admin.site.register(ReservaVisita)
admin.site.register(Exposicion)
admin.site.register(Entrada)
admin.site.register(DetalleExposicion)

# Register your models here.

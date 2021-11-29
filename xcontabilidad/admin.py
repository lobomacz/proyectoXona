from django.contrib.admin.sites import AdminSite
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.urls import reverse
from xcontabilidad.models import *

# Register your models here.

class ContabilidadAdminSite(AdminSite):
	site_header = 'Xona Admin Contab.'
	site_title = 'Admin Contabilidad'
	index_title = site_title
	site_url = reverse('index_contabilidad')


class CuentaInline(TabularInline):
	model = Cuenta
	ordering = ['catalogo', 'cuenta']


class CatalogoAdmin(ModelAdmin):
	model = Catalogo
	inlines = [
		CuentaInline
	]


class DetalleInline(TabularInline):
	model = DetalleAsiento
	ordering = ['asiento', 'movimiento', 'cuenta']


class AsientoAdmin(ModelAdmin):
	model = Asiento
	ordering = ['fecha', 'contabilizado']
	inlines = [
		DetalleInline,
	]


class PeriodoInline(TabularInline):
	model = Periodo
	ordering = ['ejercicio', 'fecha_inicio']


class EjercicioAdmin(ModelAdmin):
	model = Ejercicio
	ordering = ['activo']
	inlines = [
		PeriodoInline,
	]








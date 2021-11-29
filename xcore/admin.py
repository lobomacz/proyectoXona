from django.contrib.admin.sites import AdminSite
from django.contrib.admin import ModelAdmin, TabularInline
from django.urls import reverse
from xcore.models import *

# Register your models here.

class CoreAdminSite(AdminSite):

	site_header = 'Xona Admin Principal'
	site_title = 'Xona Core Admin'
	index_title = site_title
	site_url = reverse('index_core')


class DetalleTablaInline(TabularInline):
	model = DetalleTabla
	ordering = ['tabla', 'elemento']


class TablaAdmin(ModelAdmin):
	model = Tabla
	ordering = ['tabla']
	inlines = [
		DetalleTablaInline,
	]
	

class UsuarioAdmin(ModelAdmin):
	model = Usuario




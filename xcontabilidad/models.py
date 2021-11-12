from django.db import models
from django.utils import timezone
from django_timestamps.timestamps import TimestampsModel
from django_timestamps.softDeletion import SoftDeletionModel
from xcore.models import *

grupos = [
	('Act', 'Activo'),('Pas', 'Pasivo'),('Cap', 'Capital'),
	('Ing', 'Ingresos'),('Gas','Gastos'),('CdV', 'Costos de Venta'),
	('CdP','Costos de Producción'),('CoD','Cuentas de Orden Deudoras'),
	('CoA','Cuentas de Orden Acreedoras'),
]

# Create your models here.

class Catalogo(TimestampsModel):
	"""
	Clase para el registro del catálogo contable
	"""

	entidad = models.ForeignKey(Entidad, on_delete=models.RESTRICT)
	descripcion = models.CharField('Descripción', max_length=250)
	principal = models.BooleanField('Catálogo Principal', default=True)
	activo = models.BooleanField(default=True)

	def __str__(self):
		return self.descripcion.upper()


class Cuenta(SoftDeletionModel, TimestampsModel):
	"""
	Clase para el registro de las cuentas contables
	"""
	cuenta = models.CharField(max_length=45, primary_key=True)
	catalogo = models.ForeignKey(Catalogo, on_delete=models.PROTECT)
	grupo = models.CharField(max_length=3, choices=grupos, default='Act')
	tipo_movimiento = models.CharField('Saldo', max_length=2,choices=[('cr', 'Acreedor'),('db', 'Deudor')])
	cuenta_padre = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
	nivel = models.CharField(choices=[('C', 'Cuenta'), ('S', 'Subcuenta'), ('D', 'Detalle')])
	resumen = models.BooleanField('Cuenta de Resumen', default=False)
	cerrada = models.BooleanField(default=False)

	def __str__(self):
		return self.cuenta

	class Meta:
		ordering = ['catalogo','cuenta']
		permissions = ['cerrar_cuenta', 'Cerrar Cuenta']
		verbose_name = 'Cuenta contable'
		verbose_name_plural = 'Cuentas contables'
		constraints = [
			models.UniqueConstraint(fields=['cuenta','catalogo'], name='unique_catalogo_cuenta')
		]



class Asiento(SoftDeletionModel, TimestampsModel):
	"""
	Clase para el registro de asientos contables
	"""

	fecha = models.DateField()
	descripcion = models.CharField(max_length=300)
	referencia = models.CharField(max_length=45)
	observaciones = models.CharField(max_length=600)
	contabilizado = models.BooleanField(default=False)
	fecha_contabilizado = models.DateTimeField(null=True)
	contabilizado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, related_name='asientos_contabilizados')
	anulado = models.BooleanField(default=False)
	anulado_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT, null=True, related_name='asientos_anulados')
	fecha_anulado = models.DateTimeField(null=True)
	

	class Meta:
		ordering = ['id', 'fecha']
		verbose_name = 'Asiento Contable'
		verbose_name_plural = 'Asientos Contables'
		indexes = [
			models.Index(fields=['referencia'])
		]
		permissions = [
			('contabilizar_asiento', 'Contabilizar Asientos'),
			('anular_asiento', 'Anular Asiento Contable'),
		]

	def __str__(self):
		return "{0} - {1}".format(self.fecha, self.descripcion)


class DetalleAsiento(models.Model):
	"""Modelo de datos para DetalleAsiento"""
	asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
	cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)
	movimiento = models.CharField(choices=[('db', 'Débito'), ('cr', 'Crédito')], max_length=2)
	monto = models.DecimalField(max_digits=6, decimal_places=2)

	class Meta:
		ordering = ['cuenta', 'movimiento']
		verbose_name = 'Detalle de Asiento'
		constraints = [
			models.UniqueConstraint(fields=['asiento', 'cuenta'], name='unique_asiento_cuenta')
		]
		


class Ejercicio(models.Model):
	""" Modelo de datos para Ejercicios Contables """
	ejercicio = models.CharField(max_length=4, min_length=4)
	descripcion = models.CharField(max_length=200)
	activo = models.BooleanField(default=False)

	class Meta:
		ordering = ['ejercicio']
		verbose_name = 'Ejercicio Contable'
		verbose_name_plural = 'Ejercicios Contables'


	def get_absolute_url(self):
		return reverse('vDetalleEjercicio', {'_id':self.ejercicio})

	def __str__(self):
		return self.ejercicio


class Periodo(models.Model):
	"""Modelo de datos para PeriodoContable"""
	ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT, on_update=models.CASCADE)
	nombre = models.CharField(max_length=15)
	nombre_corto = models.CharField(max_length=3, min_length=3)
	fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
	fecha_final = models.DateField(verbose_name='Fecha Final')
	activo = models.BooleanField(default=False)
	cerrado = models.BooleanField(default=False)

	class Meta:
		ordering = ['ejercicio', 'fecha_inicio', 'activo']
		verbose_name = 'Período Contable'
		verbose_name_plural = 'Períodos Contables'
		permissions = [
			('activar_periodo', 'Activar períodos contables'),
			('cerrar_periodo', 'Cerrar períodos contables'),
			('reporte_periodo', 'Ver reportes del periodo'),
		]


	def __str__(self):
		return self.nombre







	

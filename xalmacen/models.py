from django.db import models
from django.utils import timezone
from django_timestamps.timestamps import TimestampsModel
from django_timestamps.softDeletion import SoftDeletionModel
from xcore.models import Entidad, Usuario, Producto, DetalleTabla
from xcontabilidad.models import Cuenta, Asiento

# Create your models here.

class Almacen(TimestampsModel):
	"""
	Clase para el registro de almacenes
	"""
	entidad = models.ForeignKey(Entidad, on_delete=models.RESTRICT)
	cuenta = models.ForeignKey(Cuenta, on_delete=models.RESTRICT)
	descripcion = models.CharField('Descripción', max_length=150)
	ubicacion = models.CharField('Ubicación', max_length=150)

	def __str__(self):
		return self.descripcion.upper()

	class Meta:
		ordering = ['entidad', 'cuenta']


class EntradaAlmacen(TimestampsModel):
	"""
	Clase para el registro de las entradas de almacén.
	"""
	fecha_hora = models.DateTimeField(default=timezone.now)
	almacen = models.ForeignKey(Almacen, on_delete=models.RESTRICT)
	concepto = models.CharField(max_length=150)
	referencia = models.CharField(max_length=50)
	observaciones = models.CharField(max_length=150)
	digitador = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
	asiento = models.ForeignKey(Asiento, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return "{0} {1}".format(self.fecha_hora, self.concepto).upper()

	class Meta:
		ordering = ['almacen', '-fecha_hora']


class SalidaAlmacen(EntradaAlmacen):
	"""
	Clase para el registro de las salidas de almacén.
	"""

class BaseDetalle(TimestampsModel):
	"""
	Clase base de los detalles de entrada y salida de almacén
	"""
	producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
	unidad = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT)
	cantidad = models.SmallIntegerField()
	costo = models.DecimalField('Precio de Costo', max_digits=8, decimal_places=2)
	total = models.DecimalField(max_digits=8, decimal_places=2)


class DetalleEntrada(BaseDetalle):
	"""
	Clase para el registro del detalle de entradas de almacén.
	"""
	entrada = models.ForeignKey(EntradaAlmacen, on_delete=models.CASCADE)

	def __str__(self):
		return "{0} {1} {2}".format(self.producto, self.cantidad, self.precio)

	class Meta:
		ordering = ['entrada', 'producto']


class DetalleSalida(BaseDetalle):
	"""
	Clase para el registro del detalle de salidas de almacén.
	"""
	salida = models.ForeignKey(SalidaAlmacen, on_delete=models.CASCADE)

	def __str__(self):
		return "{0} {1} {2}".format(self.producto, self.cantidad, self.precio)

	class Meta:
		ordering = ['salida', 'producto']







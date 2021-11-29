from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

# Create your models here.

class Tabla(TimestampsModel):
	"""
	Clase para registrar colecciones genéricas en tabla relacionada.
	"""
	tabla = models.CharField(max_length=45)


class DetalleTabla(TimestampsModel):
	"""
	Clase relacionada a Tabla para agrupar registros genéricos.
	"""
	tabla = models.ForeingKey(Tabla, on_delete=models.CASCADE)
	elemento = models.CharField(max_length=100)
	codigo_eq = models.CharField('Código de Equivalencia', max_length=25)


class Telefono(models.Model):
	"""
	Clase para el registro de los números de teléfono de todos los modelos.
	"""
	numero = models.CharField(
		'Número',
		max_length=9,
		validators=[RegexValidator(
			regex=r'[0-9]{4}-[0-9]{4}',
			message='El valor no es un número de teléfono válido.')], 
		help_text='Teléfono en forma 8888-8888')
	tipo = models.CharField(max_length=3, choices=[('con', 'Convencional'), ('mov', 'Móvil')], default='con')
	operador = models.ForeingKey(DetalleTabla, on_delete=models.SET_NULL, null=True)


class Entidad(TimestampsModel):
	"""
	Clase para registrar las entidades comerciales o empresas.
	"""

	logo = models.ImageField('Logotipo', upload_to='core/logos/', max_length=200)
	nombre = models.CharField('Razón Social', max_length=300)
	siglas = models.CharField('Siglas', max_length=45, null=True, blank=True)
	sector = models.ForeingKey(DetalleTabla, on_delete=models.SET_NULL, null=True)
	direccion = models.CharField('Dirección', max_length=500, null=True, blank=True)
	moneda = models.ForeingKey(DetalleTabla, on_delete=models.SET_NULL, null=True, related_name='entidades_monedas')
	

	def __str__(self):
		return self.nombre.upper()


class Usuario(SoftDeletionModel):
	"""
	Clase para registrar usuarios por Entidad correspondiente.
	"""
	
	cargo = models.ForeingKey(DetalleTabla, on_delete=models.RESTRICT, related_name='usuarios_cargo')
	telefonos = models.ManyToManyField(Telefono)
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	entidad = models.ForeingKey(Entidad, on_delete=models.CASCADE)
	rol = models.ForeingKey(DetalleTabla, on_delete=models.RESTRICT, related_name='usuarios_rol')

	def __str__(self):
		return "{0} {1}".format(self.user.first_name, self.user.last_name).upper()


class Conversion(models.Model):
	"""
	Clase para registrar las conversiones entre unidades de medida
	"""
	origen = models.ForeingKey(DetalleTabla, on_delete=models.RESTRICT, related_name='conversiones_origen')
	destino = models.ForeingKey(DetalleTabla, on_delete=models.RESTRICT, related_name='conversiones_destino')
	relacion_directa = models.DecimalField(max_digits=8, decimal_places=4)
	relacion_inversa = models.DecimalField(max_digits=8, decimal_places=4)

	class Meta:
		ordering = ['origen']
		verbose_name = 'Conversión de Unidades'
		verbose_name_plural = 'Conversiones de Unidades'

	def __str__(self):
		return "{0} - {1}".format(self.origen.elemento.upper(), self.destino.elemento.upper())


class Producto(SoftDeletionModel):
	"""
	Clase para el registro de los productos de venta
	"""

	codigo = models.SmallIntegerField('Código', null=True)
	descripcion = models.CharField('Descripción', max_length=100)
	categoria = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, related_name='categoria_producto', null=True)
	unidad = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, null=True, related_name='unidad_producto')
	precio = models.DecimalField('Precio Base', max_digits=6, decimal_places=2)
	minimo = models.IntegerField('Existencia Mínima', null=True)
	maximo = models.IntegerField('Existencia Máxima', null=True)

	def __str__(self):
		return self.descripcion.upper()

	class Meta:
		ordering = ['categoria', 'descripcion']


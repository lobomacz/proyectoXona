from django.db import models
from django.utils import timezone
from django_timestamps.timestamps import TimestampsModel
from django_timestamps.softDeletion import SoftDeletionModel
from xcore.models import Usuario, Entidad, DetalleTabla, Telefono, Producto
from xcontabilidad.models import Cuenta, Asiento

# Create your models here.


class Mesero(SoftDeletionModel, models.Model):
	"""
	Clase para el registro de los meseros y meseras.
	"""
	entidad = models.ForeignKey(Entidad, on_delete=models.RESTRICT)
	cedula = models.CharField('Cédula', max_length=16, primary_key=True)
	nombres = models.CharField(max_length=45)
	apellidos = models.CharField(max_length=45)
	telefonos = models.ManyToManyField(Telefono)
	direccion = models.TextField('Dirección')
	fecha_ingreso = models.DateField('Fecha de Ingreso')

	def __str__(self):
		return "{0} {1}".format(self.nombres, self.apellidos).upper()

	class Meta:
		ordering = ['apellidos']


class Comanda(TimestampsModel):
	"""
	Clase para el registro de las comandas del restaurante.
	"""
	fecha_hora = models.DateTimeField(auto_now_add=True)
	mesa = models.SmallIntegerField()
	mesero = models.ForeignKey(Mesero, on_delete=models.RESTRICT)
	digitador = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
	venta = models.ForeignKey('Venta', on_delete=models.SET_NULL, null=True)
	entregado = models.BooleanField()
	procesado = models.BooleanField()

	def __str__(self):
		return "Mesa {0}|{1}".format(self.mesa, self.fecha_hora)

	class Meta:
		ordering = ['mesa', 'fecha_hora']

class DetalleComanda(SoftDeletionModel, TimestampsModel):
	"""
	Clase para registrar las líneas de detalle de las comandas.
	"""
	comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
	cantidad = models.SmallIntegerField()
	precio = models.DecimalField('Precio Unitario', max_digits=8, decimal_places=2)


class Venta(models.Model):
	"""
	Clase para el registro de las ventas
	"""
	fecha_hora = models.DateTimeField(auto_now_add=True)
	mesa = models.SmallIntegerField()
	cliente = models.CharField(max_length=100, null=True)
	observaciones = models.CharField(max_length=250, null=True)
	digitador = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
	recibido = models.DecimalField(max_digits=8, decimal_places=2)
	cambio = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	forma_pago = models.CharField('Forma de Pago', max_length=2, choices=[
			('ef', 'Efectivo'),
			('tr', 'Tarjeta'),
			('cr', 'Crédito'),
		])
	cancelado = models.BooleanField()
	factura = models.ForeignKey('Factura', on_delete=models.SET_NULL, null=True)
	asiento = models.ForeignKey(Asiento, on_delete=models.RESTRICT)

	def __str__(self):
		return "{0}>>{1}>>{2}".format(self.mesa, self.fecha_hora, self.subtotal)

	class Meta:
		ordering = ['fecha_hora']


class DetalleVenta(models.Model):
	"""
	Clase para el registro del detalle de ventas.
	"""

	venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
	cantidad = models.SmallIntegerField()
	precio = models.DecimalField('Precio Unitario', max_digits=8, decimal_places=2)
	descuento = models.FloatField(null=True)
	total = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return "{0}=>{1}:: C${2}".format(self.cantidad, self.producto.descripcion, self.precio).upper()



class Factura(models.Model):
	"""
	Clase para el registro de facturas
	"""
	fecha = models.DateField()
	no_documento = models.CharField(max_length=10, null=True)
	cliente = models.CharField(max_length=150)
	id_cliente = models.CharField('Cédula/RUC', max_length=50, null=True)
	telefono = models.CharField('Teléfono', max_length=25, null=True)
	tipo = models.CharField(verbose_name='tipo de factura', choices=[('cr', 'Credito'), ('ct', 'Contado')], max_length=2)
	tipo_pago = models.CharField(verbose_name='forma de pago', choices=[('ef', 'Efectivo'), ('tr', 'Tarjeta')], max_length=2, null=True)
	descuento = models.DecimalField(max_digits=8, decimal_places=2)
	cancelada = models.BooleanField(default=False)
	observaciones = models.CharField(max_length=250, null=True)
	anulada_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='facturas_anuladas_usuario', null=True)
	fecha_anulada = models.DateField(null=True)
	digitador = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name='facturas_usuario')
	

	def __str__(self):
		return "{0} {1} C${2}".format(self.fecha, self.cliente, self.detallefactura_set.aggregate(Sum('total')))

	class Meta:
		ordering = ['fecha','tipo','cancelada']
		permissions = [
			('view_all_factura', 'Ver todas las facturas'),
			('anular_factura', 'Anular facturas'),
			('cancelar_factura', 'Cancelar facturas'),
		]
		indexes = [
			models.Index(fields=['no_documento', 'tipo', 'vendedor'])
		]
		

class DetalleFactura(models.Model):
	"""Modelo DetalleFactura asociado al modelo Factura"""
	factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
	cantidad = models.SmallIntegerField()
	precio = models.DecimalField('Precio Unitario', max_digits=8, decimal_places=2)
	descuento = models.FloatField(null=True)
	total = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return "{0} {1} {2}".format(self.producto, self.cantidad, self.total).upper()

	class Meta:
		ordering = ['factura', 'producto']
		verbose_name = 'Detalle de Factura'
		verbose_name_plural = 'Detalles de Factura'
		constraints = [
			models.UniqueConstraint(fields=['factura', 'producto'], name='unique_factura_producto')
		]


class Caja(TimestampsModel):
	"""
	Clase para el registro de caja
	"""
	cuenta = models.ForeignKey(Cuenta, on_delete=models.RESTRICT)
	descripcion = models.CharField('Descripción', max_length=150)
	saldo = models.DecimalField(max_digits=8, decimal_places=2)
	ultimo_arqueo = models.DateTimeField(default=timezone.now)
	habilitada = models.BooleanField(default=True)
	abierta = models.BooleanField(default=True)

	def __str__(self):
		return "{0} {1}".format(self.cuenta, self.descripcion).upper()


	class Meta:
		ordering = ['cuenta']



class MovimientoCaja(TimestampsModel):
	"""
	Clase para el registro de los movimientos de caja
	"""

	caja = models.ForeignKey(Caja, on_delete=models.RESTRICT)
	fecha_hora = models.DateTimeField(auto_now_add=True)
	tipo = models.CharField('Tipo de Movimiento', max_length=1, choices=[('e', 'Entrada'), ('s', 'Salida')], default='e')
	monto = models.DecimalField(max_digits=8, decimal_places=2)
	concepto = models.CharField(max_length=200)
	referencia = models.CharField(max_length=50, null=True)
	asiento = models.ForeignKey(Asiento, on_delete=models.RESTRICT)
	digitador = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
	arqueado = models.BooleanField(default=False)

	def __str__(self):
		return "{0} {1} {2}".format(self.fecha_hora, self.tipo, self.monto)

	class Meta:
		ordering = ['caja', 'tipo', '-fecha_hora']



class Arqueo(TimestampsModel):
	"""
	Clase para el registro de los arqueos de caja
	"""

	fecha_hora = models.DateTimeField(auto_now_add=True)
	caja = models.ForeignKey(Caja, on_delete=models.RESTRICT)
	saldo_caja = models.DecimalField('Saldo en Caja', max_digits=8, decimal_places=2)
	digitador = models.ForeignKey(Usuario, on_delete=models.RESTRICT)

	def __str__(self):
		return "{0}>>{1}>>{2}".format(self.caja.id, self.fecha_hora, self.digitador.user.email)

	class Meta:
		ordering = ['caja', 'fecha_hora']



class DetalleArqueo(TimestampsModel):
	"""
	Clase para el registro del detalle de los arqueos de caja
	"""

	arqueo = models.ForeignKey(Arqueo, on_delete=models.CASCADE)
	item = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT)
	cantidad = models.SmallIntegerField()
	monto = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return "{0} {1} {2}".format(self.item.elemento, self.cantidad, self.monto).upper()

	class Meta:
		ordering = ['arqueo', 'item__elemento']











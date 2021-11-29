from rest_framework import serializers
from xcore.models import Entidad, DetalleTabla, Usuario, Telefono, Producto
from xcontabilidad.models import Cuenta, Asiento, DetalleAsiento
from xventas.models import *

# Serializadores

# Serializador de Mesero
class sMesero(serializers.ModelSerializer):

	entidad = serializers.PrimaryKeyRelatedField(queryset=Entidad.objects.all())
	telefonos = serializers.PrimaryKeyRelatedField(queryset=Telefono.objects.all(), many=True)

	class Meta:
		model = Mesero
		fields = '__all__'


# Serializador de Detalle de Comanda
class sDetalleComanda(serializers.ModelSerializer):

	comanda = serializers.PrimaryKeyRelatedField(queryset=Comanda.objects.all())
	producto = serializers.PrimaryKeyRelatedField(queryset=DetalleTabla.objects.all())

	class Meta:
		model = DetalleComanda
		fields = '__all__'


# Serializador de Comanda
class sComanda(serializers.ModelSerializer):

	mesero = serializers.PrimaryKeyRelatedField(queryset=Mesero.objects.all())
	venta = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all(), allow_null=True)
	digitador = serializers.ReadOnlyField(source='digitador.user.email')
	detalle = sDetalleComanda(many=True, read_only=True)

	class Meta:
		model = Comanda 
		fields = '__all__'


#Serializador de Detalle de Venta
class sDetalleVenta(serializers.ModelSerializer):

	venta = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all())
	producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

	class Meta:
		model = DetalleVenta
		fields = '__all__'


# Serializador de Venta
class sVenta(serializers.ModelSerializer):

	digitador = serializers.ReadOnlyField(source='digitador.user.email')
	factura = serializers.PrimaryKeyRelatedField(queryset=Factura.objects.all(), allow_null=True)
	asiento = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all())
	comandas = sComanda(many=True, read_only=True)
	detalle = sDetalleVenta(many=True, read_only=True)

	class Meta:
		model = Venta
		fields = '__all__'


# Serializador para Detalle de Factura
class sDetalleFactura(serializers.ModelSerializer):

	factura = serializers.PrimaryKeyRelatedField(queryset=Factura.objects.all())
	producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

	class Meta:
		model = DetalleFactura
		fields = '__all__'


# Serializador de Factura
class sFactura(serializers.ModelSerializer):

	digitador = serializers.ReadOnlyField(source='digitador.user.email')
	detalle = sDetalleFactura(many=True, read_only=True)

	class Meta:
		model = Factura
		exclude = ['anulada', 'fecha_anulada']


# Serializador de Movimientos de Caja
class sMovimientoCaja(serializers.ModelSerializer):

	caja = serializers.PrimaryKeyRelatedField(queryset=Caja.objects.all())
	asiento = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all())
	digitador = serializers.ReadOnlyField(source='digitador.user.email')

	class Meta:
		model = MovimientoCaja
		fields = '__all__'


# Serializador de Caja
class sCaja(serializers.ModelSerializer):

	cuenta = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.all())

	class Meta:
		model = Caja
		fields = '__all__'


# Serializador de Detalle de Arqueo
class sDetalleArqueo(serializers.ModelSerializer):

	arqueo = serializers.PrimaryKeyRelatedField(queryset=Arqueo.objects.all())

	class Meta:
		model = DetalleArqueo
		fields = '__all__'



# Serializador de Arqueo
class sArqueo(serializers.ModelSerializer):

	caja = serializers.PrimaryKeyRelatedField(queryset=Caja.objects.all())
	digitador = serializers.ReadOnlyField(source='digitador.user.email')
	detalle = sDetalleArqueo(many=True, read_only=True)

	class Meta:
		model = Arqueo
		fields = '__all__'















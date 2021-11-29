from rest_framework import serializers
from xcore.models import DetalleTabla, Entidad, Usuario, Producto
from xcontabilidad.models import Cuenta, Asiento
from xalmacen.models import *


# Serializadores

# Serializador de Almacen
class sAlmacen(serializers.ModelSerializer):

	entidad = serializers.PrimaryKeyRelatedField(queryset=Entidad.objects.all())
	cuenta = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.all())

	class Meta:
		model = Almacen
		fields = '__all__'


# Serializador de Detalle de Entrada
class sDetalleEntrada(serializers.ModelSerializer):

	entrada = serializers.PrimaryKeyRelatedField(queryset=Entrada.objects.all())
	producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
	unidad = serializers.PrimaryKeyRelatedField(queryset=DetalleTabla.objects.all())

	class Meta:
		model = DetalleEntrada
		fields = '__all__'


# Serializador de Entrada de Almacen
class sEntrada(serializers.ModelSerializer):

	almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
	asiento = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all())
	digitador = serializers.ReadOnlyField(source='digitador.user.email')
	detalle = sDetalleEntrada(many=True, read_only=True)

	class Meta:
		model = Entrada
		fields = '__all__'


# Serializador de Detalle de Salida
class sDetalleSalida(serializers.ModelSerializer):

	salida = serializers.PrimaryKeyRelatedField(queryset=Salida.objects.all())
	producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
	unidad = serializers.PrimaryKeyRelatedField(queryset=DetalleTabla.objects.all())

	class Meta:
		model = DetalleSalida
		fields = '__all__'


# Serializador de Salida de Almacen
class sSalida(serializers.ModelSerializer):

	almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
	asiento = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all())
	digitador = serializers.ReadOnlyField(source='digitador.user.email')
	detalle = sDetalleSalida(many=True, read_only=True)

	class Meta:
		model = Salida
		fields = '__all__'














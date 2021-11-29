from rest_framework import serializers
from xcore.models import DetalleTabla, Entidad, Usuario
from xcontabilidad.models import *


# Serializadores

# Serializador de Cuentas
class sCuenta(serializers.ModelSerializer):

	catalogo = serializers.PrimaryKeyRelatedField(queryset=Catalogo.objects.all())
	cuenta_padre = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.all(), allow_null=True)

	class Meta:
		model = Cuenta
		fields = '__all__'

# Serializador de Catalogo
class sCatalogo(serializers.ModelSerializer):

	entidad = serializers.PrimaryKeyRelatedField(queryset=Entidad.objects.all())
	cuentas = sCuenta(many=True, read_only=True)

	class Meta:
		model = Catalogo
		fields = '__all__'


# Serializador de Detalle de Asiento para campo relacionado
class sDetalleRelated(serializers.ModelSerializer):

	asiento = serializers.StringRelatedField()
	cuenta = serializers.StringRelatedField()

	class Meta:
		model = DetalleAsiento
		fields = '__all__'


# Serializador de Asientos
class sAsiento(serializers.ModelSerializer):

	contabilizado_por = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), allow_null=True)
	anulado_por = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), allow_null=True)
	detalle = sDetalleRelated(many=True, read_only=True)

	class Meta:
		model = Asiento
		fields = '__all__'

# Serializador de Detalle de Asientos
class sDetalleAsiento(serializers.ModelSerializer):

	asiento = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all())
	cuenta = serializers.PrimaryKeyRelatedField(queryset=Cuenta.objects.all())

	class Meta:
		model = Asiento
		fields = '__all__'


# Serializador de Períodos para relacionar
class sPeriodo(serializers.ModelSerializer):

	ejercicio = serializers.PrimaryKeyRelatedField(queryset=Ejercicio.objects.all())

	class Meta:
		model = Periodo
		'__all__'

# Serializador de Ejercicio contable
class sEjercicio(serializers.ModelSerializer):

	periodos = sPeriodo(many=True, read_only=True)

	class Meta:
		model = Ejercicio
		fields = '__all__'







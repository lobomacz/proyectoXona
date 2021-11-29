from rest_framework import serializers
from django.contrib.auth.models import User
from xcore.models import *


# Serializadores

# Serializador para DetalleTabla
class sDetalleTabla(serializers.ModelSerializer):

	class Meta:
		model = DetalleTabla
		fields = '__all__'


# Serializador de Entidad
class sEntidad(serializers.ModelSerializer):

	class Meta:
		model = Entidad
		fields = '__all__'


# Serializador de Telefono
class sTelefono(serializers.ModelSerializer):

	class Meta:
		model = Telefono
		fields = '__all__'


# Serializador de Usuario
class sUsuario(serializers.ModelSerializer):

	user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
	entidad = serializers.PrimaryKeyRelatedField(many=False, queryset=Entidad.objects.all())
	telefonos = serializers.PrimaryKeyRelatedField(queryset=Telefono.objects.all(), many=True, allow_null=True)

	class Meta:
		model = Usuario
		fields = '__all__'


# Serializador de Producto
class sProducto(serializers.ModelSerializer):

	categoria = serializers.PrimaryKeyRelatedField(queryset=DetalleTabla.objects.filter(tabla__tabla='categoria'), many=False, allow_null=True)
	unidad = serializers.PrimaryKeyRelatedField(queryset=DetalleTabla.objects.filter(tabla__tabla='unidad'), many=False, allow_null=True)

	class Meta:
		model = Producto
		fields = '__all__'



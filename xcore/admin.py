from django.contrib.admin.sites import AdminSite
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from xcore.models import *

# Register your models here.

class CoreAdminSite(AdminSite):
	
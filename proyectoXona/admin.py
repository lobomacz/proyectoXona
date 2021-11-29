from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from xcore.admin import *
from xcontabilidad.admin import *


# Aquí se registran los modelos en el sitio admin

 #   ____    ___    ____    _____ 
 #  / ___|  / _ \  |  _ \  | ____|
 # | |     | | | | | |_) | |  _|  
 # | |___  | |_| | |  _ <  | |___ 
 #  \____|  \___/  |_| \_\ |_____|
 #                                

core_admin = CoreAdminSite(name='coreadmin')

core_admin.register(User, UserAdmin)
core_admin.register(Tabla, TablaAdmin)
core_admin.register(Usuario, UsuarioAdmin)
core_admin.register(Entidad)
core_admin.register(Producto)
core_admin.register(Conversion)


 #   ____    ___    _   _   _____      _      ____    ___   _       ___   ____       _      ____  
 #  / ___|  / _ \  | \ | | |_   _|    / \    | __ )  |_ _| | |     |_ _| |  _ \     / \    |  _ \ 
 # | |     | | | | |  \| |   | |     / _ \   |  _ \   | |  | |      | |  | | | |   / _ \   | | | |
 # | |___  | |_| | | |\  |   | |    / ___ \  | |_) |  | |  | |___   | |  | |_| |  / ___ \  | |_| |
 #  \____|  \___/  |_| \_|   |_|   /_/   \_\ |____/  |___| |_____| |___| |____/  /_/   \_\ |____/ 
 #                     

conta_admin = ContabilidadAdminSite(name='contabadmin')

conta_admin.register(Catalogo, CatalogoAdmin)
conta_admin.register(Asiento, AsientoAdmin)
conta_admin.register(Ejercicio, EjercicioAdmin)


 # __     __  _____   _   _   _____      _      ____  
 # \ \   / / | ____| | \ | | |_   _|    / \    / ___| 
 #  \ \ / /  |  _|   |  \| |   | |     / _ \   \___ \ 
 #   \ V /   | |___  | |\  |   | |    / ___ \   ___) |
 #    \_/    |_____| |_| \_|   |_|   /_/   \_\ |____/ 
 #



 #     _      _       __  __      _       ____   _____   _   _ 
 #    / \    | |     |  \/  |    / \     / ___| | ____| | \ | |
 #   / _ \   | |     | |\/| |   / _ \   | |     |  _|   |  \| |
 #  / ___ \  | |___  | |  | |  / ___ \  | |___  | |___  | |\  |
 # /_/   \_\ |_____| |_|  |_| /_/   \_\  \____| |_____| |_| \_|
 #                                                            




















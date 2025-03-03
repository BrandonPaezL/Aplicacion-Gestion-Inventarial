"""
URL configuration for Inventario_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dashboard import views


from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('grupos/', views.grupos, name='grupos'),
    path('crear_grupo/', views.crear_grupo, name='crear_grupo'),
    path('medicamentos_caducar/', views.alertas, name='medicamentos_caducar'),
    path('audit-log/', views.audit_log_view, name='audit_log'),
    path('presupuesto/', views.presupuesto, name='presupuesto'),
    path('contacto/', views.contacto, name='contacto'),
    path('reportes/', views.reportes, name='reportes'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('alertas/', views.alertas, name='alertas'),
    path('entrega_elementos/', views.entrega_elementos, name='entrega_elementos'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('cronograma/', views.cronograma, name='cronograma'),
    path('cronograma/agregar/', views.agregar_entrega, name='agregar_entrega'),
    path('cronograma/editar/<int:entrega_id>/', views.editar_entrega, name='editar_entrega'),
    path('cronograma/eliminar/<int:entrega_id>/', views.eliminar_entrega, name='eliminar_entrega'),
    path('cronograma/calendario/', views.vista_calendario, name='vista_calendario'),
    path('buscar/', views.buscar, name='buscar'),
    path('buscar_sugerencias/', views.buscar_sugerencias, name='buscar_sugerencias'),
]



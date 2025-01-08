from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    fecha_caducidad = models.DateField()
    categoria = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



# Modelo de Grupo
class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#FFFFFF')  # Código de color en hexadecimal
    medicamentos = models.ManyToManyField(Producto, related_name='grupos')

    def __str__(self):
        return self.nombre


# Modelo de Venta
class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.PositiveIntegerField()
    factura_id = models.CharField(max_length=50, null=True, blank=True)
    fecha_venta = models.DateField(default=timezone.now)
    destinatario = models.CharField(max_length=100, default='') 

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"


# Modelo de Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.TextField()

    def __str__(self):
        return self.nombre


# Modelo de Usuario (si no usas el sistema de usuarios de Django directamente)
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('usuario', 'Usuario')])

    def __str__(self):
        return self.nombre


# Modelo de Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()

    def __str__(self):
        return self.nombre

from django.db import models

class Medicamento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_caducidad = models.DateField()
    cantidad_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Presupuesto(models.Model):
    monto_disponible = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Presupuesto: {self.monto_disponible} CLP"
    

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.date}"
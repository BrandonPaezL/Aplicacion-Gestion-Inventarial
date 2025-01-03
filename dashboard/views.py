from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Medicamento, Presupuesto, Producto, Grupo  # Usamos los modelos reales definidos en models.py
from .forms import ProductoForm, GrupoForm
from django.db.models import Sum  # Para realizar agregaciones como sumas
from django.db.models import Count

# Vista principal
def index(request):
    return render(request, 'index.html')

# Sección principal de inventario
def lista_inventario(request):
    productos = Producto.objects.all()
    return render(request, 'inventario.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_inventario')
    else:
        form = ProductoForm()
    return render(request, 'add_producto.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return redirect('lista_productos')

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    return redirect('lista_inventario')

# Medicinas disponibles
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos_disponibles.html', {'productos': productos})

def inventario(request):
    total_medicamentos = Producto.objects.count()
    return render(request, 'inventario.html', {'total_medicamentos': total_medicamentos})

# Grupos de productos
def grupos(request):
    grupos = Grupo.objects.all()[:8]
    return render(request, 'grupos.html', {'grupos': grupos})

def crear_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grupos')
    else:
        form = GrupoForm()
    return render(request, 'crear_grupo.html', {'form': form})

# Log de auditoría
def audit_log(request):
    audit_logs = []
    return render(request, 'audit_log.html', {'audit_logs': audit_logs})

# Presupuesto
def presupuesto(request):
    return render(request, 'presupuesto.html')

# Contacto
def contacto(request):
    return render(request, 'contacto.html')

# Dashboard
def dashboard(request):
    total_medicines = Producto.objects.count()
    proximos_a_vencer_count = Producto.objects.filter(
        fecha_caducidad__lte=timezone.now().date() + timedelta(days=30)
    ).count()

    context = {
        'total_medicines': total_medicines,
        'proximos_a_vencer_count': proximos_a_vencer_count,
    }
    return render(request, 'dashboard/index.html', context)

def reportes(request):
    return render(request, 'reportes.html')

# Umbrales configurables
UMBRAL_CADUCIDAD_DIAS = 21  # 3 semanas
UMBRAL_STOCK_BAJO = 30

# Alertas
def alertas(request):
    hoy = timezone.now().date()
    umbral_caducidad = hoy + timedelta(days=UMBRAL_CADUCIDAD_DIAS)

    # Filtrar productos próximos a caducar (dentro de 3 semanas)
    productos_caducar = Producto.objects.filter(
        fecha_caducidad__lte=umbral_caducidad,
        fecha_caducidad__gte=hoy
    )

    # Filtrar productos con stock bajo (menos de 30 unidades)
    productos_stock_bajo = Producto.objects.filter(
        cantidad__lt=UMBRAL_STOCK_BAJO
    )

    context = {
        'productos_caducar': productos_caducar,
        'productos_stock_bajo': productos_stock_bajo,
    }

    return render(request, 'alertas.html', context)


def reportes(request):
    # Obtener todas las categorías únicas
    categorias = Producto.objects.values_list('categoria', flat=True).distinct()

    # Filtrar por categoría seleccionada
    categoria_seleccionada = request.GET.get('categoria')
    if categoria_seleccionada:
        productos = Producto.objects.filter(categoria=categoria_seleccionada)
    else:
        productos = Producto.objects.all()

    # Datos para el gráfico (productos por categoría)
    datos_grafico = Producto.objects.values('categoria').annotate(total=Count('id'))

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'datos_grafico': datos_grafico,
    }

    return render(request, 'reportes.html', context)

def inventario_dashboard(request):
    total_medicamentos = Medicamento.objects.count()
    grupos_medicamentos = Grupo.objects.all()
    return render(request, 'index.html', {
        'total_medicamentos': total_medicamentos,
        'grupos_medicamentos': grupos_medicamentos
    })
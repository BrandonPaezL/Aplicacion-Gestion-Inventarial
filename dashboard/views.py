from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import AuditLog, Medicamento, Presupuesto, Producto, Grupo, Venta # Usamos los modelos reales definidos en models.py
from .forms import ProductoForm, GrupoForm, EntregaElementosForm, LoginForm, RegistroForm
from django.db.models import Sum  # Para realizar agregaciones como sumas
from django.db.models import Count # Para realizar agregaciones como contar
from django.contrib.auth import authenticate, login, logout # Para autenticar usuarios
from django.contrib.auth.decorators import login_required # Para proteger vistas con autenticación
from django.contrib import messages 



# Vista principal
@login_required
def index(request):
    return render(request, 'index.html')

# Sección principal de inventario
@login_required
def lista_inventario(request):
    productos = Producto.objects.all()
    return render(request, 'inventario.html', {'productos': productos})
@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_inventario')
    else:
        form = ProductoForm()
    return render(request, 'add_producto.html', {'form': form})

@login_required
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

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    return redirect('lista_inventario')

# Medicinas disponibles
@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos_disponibles.html', {'productos': productos})

@login_required
def inventario(request):
    total_medicamentos = Producto.objects.count()
    return render(request, 'inventario.html', {'total_medicamentos': total_medicamentos})

# Grupos de productos
@login_required
def grupos(request):
    grupos = Grupo.objects.all()[:8]
    return render(request, 'grupos.html', {'grupos': grupos})

@login_required
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
@login_required
def audit_log_view(request):
    audit_logs = AuditLog.objects.all().order_by('-date')
    return render(request, 'audit_log.html', {'audit_logs': audit_logs})

# Presupuesto
@login_required
def presupuesto(request):
    return render(request, 'presupuesto.html')

# Contacto
@login_required
def contacto(request):
    return render(request, 'contacto.html')

# Dashboard
@login_required
def dashboard(request):
    total_medicines = Producto.objects.count()
    proximos_a_vencer_count = Producto.objects.filter(
        fecha_caducidad__lte=timezone.now().date() + timedelta(days=30)
    ).count()

    context = {
        'total_medicines': total_medicines,
        'proximos_a_vencer_count': proximos_a_vencer_count,
    }
    return render(request, 'index.html', context)

@login_required
def reportes(request):
    return render(request, 'reportes.html')

# Umbrales configurables

UMBRAL_CADUCIDAD_DIAS = 21  # 3 semanas
UMBRAL_STOCK_BAJO = 30

# Alertas
@login_required
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

@login_required
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

@login_required
def inventario_dashboard(request):
    total_medicamentos = Medicamento.objects.count()
    grupos_medicamentos = Grupo.objects.all()
    return render(request, 'index.html', {
        'total_medicamentos': total_medicamentos,
        'grupos_medicamentos': grupos_medicamentos
    })


@login_required
def entrega_elementos(request):
    return render(request, 'entrega_elementos.html')


@login_required
def entrega_elementos(request):
    if request.method == 'POST':
        form = EntregaElementosForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto = venta.producto
            if producto.cantidad >= venta.cantidad:
                producto.cantidad -= venta.cantidad
                producto.save()
                venta.fecha_venta = timezone.now()
                venta.save()
                return redirect('entrega_elementos')
            else:
                form.add_error('cantidad', 'Cantidad insuficiente en inventario')
    else:
        form = EntregaElementosForm()
    return render(request, 'entrega_elementos.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el usuario
            # Agrega un mensaje para mostrar en la vista de login
            messages.success(request, 'Usuario registrado satisfactoriamente.')
            return redirect('login')  # Redirige a la vista de login
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
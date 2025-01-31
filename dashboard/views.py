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
from .models import Entrega
from django.http import JsonResponse
from django.shortcuts import reverse
from .models import Producto  # Modelo de productos

def registrar_auditoria(user, action):
    AuditLog.objects.create(user=user, action=action, date=timezone.now())

# Vista principal
@login_required
def index(request):
    # Obtener la cantidad de productos en inventario
    cantidad_inventario = Producto.objects.count()

    # Obtener la última entrega
    ultima_entrega = Entrega.objects.order_by('-fecha').first()  # Última entrega realizada

    # Obtener la próxima entrega
    proxima_entrega = Entrega.objects.filter(fecha__gte=timezone.now().date()).order_by('fecha').first()

    context = {
        'cantidad_inventario': cantidad_inventario,
        'ultima_entrega': ultima_entrega,
        'proxima_entrega': proxima_entrega,
    }

    return render(request, 'index.html', context)

@login_required
def buscar(request):
    query = request.GET.get('q', '')  # Obtiene el término de búsqueda
    resultados_productos = Producto.objects.filter(nombre__icontains=query)  # Busca productos

    context = {
        'query': query,
        'resultados_productos': resultados_productos,
    }
    return render(request, 'buscar_resultados.html', context)


@login_required
def buscar_sugerencias(request):
    query = request.GET.get('q', '').lower()
    resultados = []

    if query:
        # Búsqueda en productos
        productos = Producto.objects.filter(nombre__icontains=query)[:5]
        for producto in productos:
            resultados.append({
                "nombre": producto.nombre,
                "url": reverse("detalle_producto", args=[producto.id])
            })

        # Búsqueda en secciones predefinidas
        secciones = {
            "inventario": "/inventario/",
            "reportes": "/reportes/",
            "alertas": "/alertas/",
            "configuracion": "/configuracion/",
        }
        for key, url in secciones.items():
            if query in key:
                resultados.append({"nombre": key.capitalize(), "url": url})

    return JsonResponse({"resultados": resultados})

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
            producto = form.save()
            registrar_auditoria(request.user, f"Agregó el producto {producto.nombre}")
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
            registrar_auditoria(request.user, f"Editó el producto {producto.nombre}")
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return redirect('lista_productos')

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    registrar_auditoria(request.user, f"Eliminó el producto {producto.nombre}")
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
            grupo = form.save()
            registrar_auditoria(request.user, f"Creó el grupo {grupo.nombre}")
            return redirect('grupos')
    else:
        form = GrupoForm()
    return render(request, 'crear_grupo.html', {'form': form})

# Log de auditoría
@login_required
def audit_log_view(request):
    """
    Vista para mostrar el registro de auditoría.
    """
    audit_logs = AuditLog.objects.all().order_by('-date')  # Ordena por fecha descendente
    context = {'audit_logs': audit_logs}
    return render(request, 'audit_log.html', context)

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
                registrar_auditoria(request.user, f"Realizó una entrega del producto {producto.nombre}")
                messages.success(request, "Entrega realizada exitosamente.")
                return redirect('entrega_elementos')  # Redirige para evitar reenvío del formulario
            else:
                form.add_error('cantidad', 'Cantidad insuficiente en inventario')
        else:
            messages.error(request, "Formulario inválido. Revisa los datos ingresados.")
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
                registrar_auditoria(user, "Inició sesión")
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
            usuario = form.save()  # Guarda el usuario
            registrar_auditoria(usuario, "Registró un nuevo usuario")
            messages.success(request, 'Usuario registrado satisfactoriamente.')
            return redirect('login')  # Redirige a la vista de login
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    user = request.user
    logout(request)
    registrar_auditoria(user, "Cerró sesión")
    return redirect('login')




# Listar entregas
def cronograma(request):
    entregas = Entrega.objects.all().order_by('fecha')
    return render(request, 'cronograma.html', {'entregas': entregas})

# Agregar entrega
def agregar_entrega(request):
    if request.method == 'POST':
        fecha = request.POST['fecha']
        elemento = request.POST['elemento']
        cantidad = request.POST['cantidad']
        responsable = request.POST['responsable']
        
        Entrega.objects.create(
            fecha=fecha,
            elemento=elemento,
            cantidad=cantidad,
            responsable=responsable
        )
        registrar_auditoria(request.user, f"Agregó una entrega de {elemento}")
        return redirect('cronograma')
    return render(request, 'cronograma.html')

# Editar entrega
def editar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id)
    if request.method == 'POST':
        entrega.fecha = request.POST['fecha']
        entrega.elemento = request.POST['elemento']
        entrega.cantidad = request.POST['cantidad']
        entrega.responsable = request.POST['responsable']
        entrega.save()
        registrar_auditoria(request.user, f"Editó la entrega de {entrega.elemento}")
        return redirect('cronograma')
    return render(request, 'editar_entrega.html', {'entrega': entrega})

# Eliminar entrega
def eliminar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id)
    registrar_auditoria(request.user, f"Eliminó la entrega de {entrega.elemento}")
    entrega.delete()
    return redirect('cronograma')

def vista_calendario(request):
    entregas = Entrega.objects.all()
    return render(request, 'calendario.html', {'entregas': entregas})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario, Servicio, Mensaje, Valoracion
from .forms import RegistroForm, LoginForm, ServicioForm, MensajeForm, ValoracionForm
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import EditarPerfilForm
from core.models import Notificacion


# Home
def home(request):
    notifs = []
    if request.user.is_authenticated:
        notifs = Notificacion.objects.filter(receptor=request.user, leida=False)
    return render(request, 'home.html', {'notifs': notifs})

# Registro
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'form': form, 'error': 'Usuario o contraseña incorrecta'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# Perfil de usuario
@login_required
def profile_view(request, user_id):
    user = get_object_or_404(Usuario, id=user_id)
    return render(request, 'profile.html', {'user': user})

# Lista de servicios con filtros y paginación
@login_required
def services_view(request):
    servicios = Servicio.objects.all()
    search = request.GET.get('search')
    category = request.GET.get('category')
    location = request.GET.get('location')

    if search:
        servicios = servicios.filter(title__icontains=search)
    if category:
        servicios = servicios.filter(category=category)
    if location:
        servicios = servicios.filter(location__icontains=location)

    paginator = Paginator(servicios, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'services.html', {'services': page_obj, 'page_obj': page_obj})

# Crear servicio
@login_required
def create_service_view(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.user = request.user
            servicio.save()
            messages.success(request, "Servicio publicado correctamente ✅")
            return redirect('create_service')
        else:
            messages.error(request, "Error al publicar el servicio. Revisá los campos.")
    else:
        form = ServicioForm()
    return render(request, 'create_service.html', {'form': form})

# Chat con otro usuario
@login_required
def chat_view(request, user_id):
    chat_user = get_object_or_404(Usuario, id=user_id)

    if chat_user == request.user:
        chat_user = None
        mensajes = []
    else:
        mensajes = Mensaje.objects.filter(
            sender__in=[request.user, chat_user],
            receiver__in=[request.user, chat_user]
        )

    return render(request, 'chat.html', {'chat_user': chat_user, 'messages': mensajes})

# Términos y condiciones
def terms_view(request):
    return render(request, 'terms.html')

# Enviar mensaje
@login_required
def send_message(request, user_id):
    if request.method == "POST":
        content = request.POST.get("message", "")
        recipient = get_object_or_404(Usuario, id=user_id)
        if content:
            # Guardar mensaje
            Mensaje.objects.create(sender=request.user, receiver=recipient, content=content)
            # Crear notificación
            Notificacion.objects.create(
                receptor=recipient,
                emisor=request.user,
                mensaje=f"Te envió un mensaje: {content[:50]}"
            )
    return redirect('chat', user_id=user_id)

@login_required
def notificaciones_view(request):
    notifs = Notificacion.objects.filter(receptor=request.user).order_by('-fecha')
    return render(request, 'notificaciones.html', {'notifs': notifs})

@login_required
def marcar_leida_view(request, notif_id):
    """
    Marca una notificación como leída y redirige a la misma página de notificaciones.
    """
    notif = get_object_or_404(Notificacion, id=notif_id, receptor=request.user)
    notif.leida = True
    notif.save()
    return redirect('notificaciones')


@login_required
def valorar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if servicio.user == request.user:
        messages.error(request, "No podés valorar tu propio servicio.")
        return redirect('profile', user_id=servicio.user.id)

    if Valoracion.objects.filter(servicio=servicio, autor=request.user).exists():
        messages.error(request, "Ya valoraste este servicio.")
        return redirect('profile', user_id=servicio.user.id)

    if request.method == 'POST':
        form = ValoracionForm(request.POST)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.servicio = servicio
            valoracion.autor = request.user
            valoracion.save()
            messages.success(request, "¡Gracias por tu valoración!")
            return redirect('profile', user_id=servicio.user.id)
    else:
        form = ValoracionForm()

    return render(request, 'valorar_servicio.html', {'form': form, 'servicio': servicio})

@login_required
def edit_profile_view(request, user_id):
    user = get_object_or_404(Usuario, id=user_id)

    if request.user != user:
        messages.error(request, "No podés editar el perfil de otro usuario.")
        return redirect('profile', user_id=user.id)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'profile_image-clear' in request.POST:
                user.profile_image.delete(save=False)
                user.profile_image = None

            form.save()
            messages.success(request, "Perfil actualizado correctamente ✅")
            return redirect('profile', user_id=user.id)
    else:
        form = EditarPerfilForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form, 'user': user})
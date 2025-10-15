from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario, Servicio, Mensaje, Rol
from .forms import RegistroForm, LoginForm, ServicioForm, MensajeForm
from django.core.paginator import Paginator
from django.contrib import messages

# Home
def home(request):
    return render(request, 'home.html')

# Registro
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            if form.cleaned_data.get('roles'):
                user.roles.set(form.cleaned_data['roles'])
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
            Mensaje.objects.create(sender=request.user, receiver=recipient, content=content)
    return redirect('chat', user_id=user_id)

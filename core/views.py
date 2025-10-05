from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import random

# core/views.py
def services(request):
    users = {
        1: "Instructor de Yoga",
        2: "Profesor de Matemática",
        3: "Técnico en Computadoras",
        4: "Electricista",
        5: "Nutricionista",
    }

    predefined_services = [
        {"title": "Clases de Yoga", "category": "salud", "location": "Palermo", "user_id": 1, "rating": 4.8, "profession": users[1]},
        {"title": "Clases de Matemática", "category": "educacion", "location": "Recoleta", "user_id": 2, "rating": 4.7, "profession": users[2]},
        {"title": "Reparación de Laptops", "category": "tecnologia", "location": "Caballito", "user_id": 3, "rating": 4.9, "profession": users[3]},
        {"title": "Electricista a Domicilio", "category": "hogar", "location": "Belgrano", "user_id": 4, "rating": 4.6, "profession": users[4]},
        {"title": "Asesoramiento Nutricional", "category": "salud", "location": "Palermo", "user_id": 5, "rating": 4.9, "profession": users[5]},
    ]

    # Si generás servicios extra aleatorios
    import random
    extra_services = []
    categories = ["educacion", "hogar", "tecnologia", "salud"]
    locations = ["Palermo", "Recoleta", "Caballito", "Belgrano"]

    for i in range(5):
        user_id = random.choice(list(users.keys()))
        extra_services.append({
            "title": f"Servicio Extra {i+1}",
            "category": random.choice(categories),
            "location": random.choice(locations),
            "user_id": user_id,
            "rating": round(random.uniform(3.5, 5.0), 1),
            "profession": users[user_id]  # <-- agrego profesión
        })

    all_services = predefined_services + extra_services

    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(all_services, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'services.html', {'services': page_obj, 'page_obj': page_obj})

# -------------------------------
# HOME, LOGIN, REGISTER
# -------------------------------
def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def logout_view(request):
    return redirect('home')

# -------------------------------
# PROFILE
# -------------------------------
def profile_view(request, user_id):
    # Usuarios con profesiones coherentes
    fake_users = {
        1: {"username": "Jorge", "age": 20, "profession": "Instructor de Yoga", "location": "Palermo"},
        2: {"username": "Manuel", "age": 22, "profession": "Profesor de Matemática", "location": "Recoleta"},
        3: {"username": "Pedro", "age": 25, "profession": "Técnico en Computadoras", "location": "Caballito"},
        4: {"username": "Pablo", "age": 24, "profession": "Electricista", "location": "Belgrano"},
        5: {"username": "Laura", "age": 30, "profession": "Nutricionista", "location": "Palermo"},
    }
    user = fake_users.get(user_id)
    if not user:
        return render(request, "404.html", status=404)
    return render(request, "profile.html", {"user": user})

# -------------------------------
# CHAT
# -------------------------------
def chat(request, chat_user_id=None):
    if chat_user_id is None:
        return render(request, 'chat.html', {'message': 'Seleccioná un usuario para chatear'})
    
    messages = [
        {"sender": "Jorge", "content": "Hola!"},
        {"sender": "Tú", "content": "Hola, ¿cómo estás?"}
    ]
    chat_user = {"username": f"Usuario {chat_user_id}"}
    return render(request, 'chat.html', {'chat_user': chat_user, 'messages': messages})

def send_message(request, user_id):
    return redirect('chat_with_user', chat_user_id=user_id)



def create_service(request):
    return render(request, 'create_service.html')

def terms(request):
    return render(request, 'terms.html')

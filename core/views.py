from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def profile(request):
    return render(request, 'profile.html')

def chat(request):
    return render(request, 'chat.html')

def create_service(request):
    return render(request, 'create_service.html')

def services(request):
    return render(request, 'services.html')

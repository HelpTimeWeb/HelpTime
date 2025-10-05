from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# SERVICIOS
# -------------------------------
class Service(models.Model):
    title = models.CharField(max_length=100)       # antes "name"
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # antes "owner"

    def __str__(self):
        return self.title

# -------------------------------
# MENSAJES PARA CHAT
# -------------------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:20]}"

# -------------------------------
# MODELOS DE PRUEBA (opcionales)
# -------------------------------
class UsuarioPrueba(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class PublicacionPrueba(models.Model):
    usuario = models.ForeignKey(UsuarioPrueba, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

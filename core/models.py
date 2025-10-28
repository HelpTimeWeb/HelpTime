from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
import os
from cloudinary_storage.storage import MediaCloudinaryStorage


def profile_image_upload_path(instance, filename):
    """Guarda la imagen de perfil en Cloudinary o media/profiles/<username>/<filename>"""
    return os.path.join('profiles', instance.username, filename)

class Usuario(AbstractUser):
    profession = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    profile_image = models.ImageField(
    storage=MediaCloudinaryStorage(),  # 👈 esto fuerza Cloudinary
    upload_to=profile_image_upload_path,
    blank=True,
    null=True,
    default='profiles/default.png'
)


    @property
    def profile_image_url(self):
        """Devuelve la URL de la imagen de perfil o default.png en Cloudinary/Media"""
        try:
            if self.profile_image and hasattr(self.profile_image, 'url'):
                return self.profile_image.url
        except Exception:
            pass
        # Fallback
        if settings.DEBUG:
            return f"{settings.MEDIA_URL}profiles/default.png"
        return "https://res.cloudinary.com/dcirbnch2/image/upload/v1761276056/profiles/default.png"

    groups = models.ManyToManyField(
        Group,
        related_name="usuario_set",
        blank=True,
        help_text="Grupos a los que pertenece el usuario.",
        verbose_name="grupos"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="usuario_permissions_set",
        blank=True,
        help_text="Permisos específicos del usuario.",
        verbose_name="permisos de usuario"
    )

    def __str__(self):
        return self.username
    
    @property
    def reputacion(self):
        valoraciones = Valoracion.objects.filter(servicio__user=self)
        if not valoraciones.exists():
            return 0
        promedio = sum(v.puntuacion for v in valoraciones) / valoraciones.count()
        return round(promedio, 2)


# -------------------------------------------------------
# Servicio publicado por un usuario
# -------------------------------------------------------
class Servicio(models.Model):
    CATEGORY_CHOICES = (
        ('educacion', 'Educación'),
        ('hogar', 'Hogar'),
        ('tecnologia', 'Tecnología'),
        ('salud', 'Salud'),
    )

    image = models.ImageField(
    storage=MediaCloudinaryStorage(),
    upload_to='services/',
    blank=True,
    null=True
)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    @property
    def rating(self):
        valoraciones = self.valoraciones.all()
        if valoraciones.exists():
            return round(sum(v.puntuacion for v in valoraciones) / valoraciones.count(), 1)
        return 0


# -------------------------------------------------------
# Mensajes de chat entre usuarios
# -------------------------------------------------------
class Mensaje(models.Model):
    sender = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='enviados')
    receiver = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recibidos')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"
    

class Valoracion(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='valoraciones')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='valoraciones_realizadas')
    puntuacion = models.PositiveIntegerField(choices=[(i, f"{i} estrellas") for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('servicio', 'autor')  # evita que un usuario valore dos veces el mismo servicio

    def __str__(self):
        return f"{self.autor.username} → {self.servicio.title}: {self.puntuacion}★"
    
class Notificacion(models.Model):
    receptor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="notificaciones"
    )
    emisor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="notificaciones_enviadas"
    )
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emisor} ➔ {self.receptor}: {self.mensaje[:20]}"
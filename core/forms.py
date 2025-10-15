from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Servicio, Mensaje, Rol

# Formulario de registro
class RegistroForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    email = forms.EmailField(label="Correo electrónico", required=True)
    age = forms.IntegerField(label="Edad", required=False, min_value=0)
    profession = forms.CharField(label="Profesión", required=False, max_length=100)
    location = forms.CharField(label="Ubicación", required=False, max_length=100)
    profile_image = forms.ImageField(label="Imagen de perfil", required=False)
    roles = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Roles",
        required=False
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password1', 'password2',
            'age', 'profession', 'location', 'profile_image', 'roles'
        ]
        labels = {
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        help_texts = {
            'username': 'Máximo 150 caracteres. Solo letras, números y @/./+/-/_',
            'password1': 'Debe contener al menos 8 caracteres.',
            'password2': 'Reescriba la contraseña para confirmarla.',
        }

# Formulario de login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

# Formulario para publicar un servicio
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['title', 'description', 'category', 'profession', 'location', 'image']
        labels = {
            'title': 'Nombre del Servicio',
            'description': 'Descripción',
            'category': 'Categoría',
            'profession': 'Profesión',
            'location': 'Ubicación',
            'image': 'Imagen del Servicio',
        }
        help_texts = {
            'title': 'Ej: Clases de guitarra',
            'location': 'Ciudad o barrio',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Detalles del servicio', 'rows': 4}),
            'title': forms.TextInput(attrs={'placeholder': 'Nombre del servicio'}),
            'location': forms.TextInput(attrs={'placeholder': 'Ciudad o barrio'}),
        }

# Formulario de mensajes
class MensajeForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Escribe un mensaje...'}),
        label=''
    )

    class Meta:
        model = Mensaje
        fields = ['content']

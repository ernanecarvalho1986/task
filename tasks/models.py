from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telegram_chat_id = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Task(models.Model):
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo      = models.CharField(max_length=200)
    descricao   = models.TextField(blank=True)
    data_limite = models.DateField()
    concluida   = models.BooleanField(default=False)
    whatsapp    = models.CharField(max_length=20, blank=True, default='')
    criada_em   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

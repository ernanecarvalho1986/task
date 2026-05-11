from django.db import models

class Task(models.Model):
    titulo      = models.CharField(max_length=200)
    descricao   = models.TextField(blank=True)
    data_limite = models.DateField()
    concluida   = models.BooleanField(default=False)
    whatsapp    = models.CharField(max_length=20, help_text="Ex: 5534999998888")
    criada_em   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

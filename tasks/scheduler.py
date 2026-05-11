from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from datetime import date
from .models import Task
from .whatsapp import enviar_whatsapp

def verificar_tarefas():
    hoje = date.today()
    tarefas = Task.objects.filter(data_limite=hoje, concluida=False)
    for t in tarefas:
        msg = f"⚠️ LEMBRETE: Tarefa '{t.titulo}' vence HOJE! Conclua agora."
        enviar_whatsapp(t.whatsapp, msg, settings.CALLMEBOT_API_KEY)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_tarefas, 'cron', hour=8, minute=0)
    scheduler.start()
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from datetime import date
from .models import Task
from .whatsapp import enviar_whatsapp

logger = logging.getLogger(__name__)

def verificar_tarefas():
    logger.info("🔔 Scheduler rodando — verificando tarefas...")
    hoje = date.today()
    tarefas = Task.objects.filter(data_limite=hoje, concluida=False)
    logger.info(f"Tarefas encontradas para hoje: {tarefas.count()}")
    for t in tarefas:
        msg = f"⚠️ LEMBRETE: Tarefa '{t.titulo}' vence HOJE! Conclua agora."
        resultado = enviar_whatsapp(t.whatsapp, msg, settings.CALLMEBOT_API_KEY)
        logger.info(f"WhatsApp enviado para {t.whatsapp}: {resultado}")

def start():
    logger.info("✅ Iniciando scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_tarefas, 'cron', hour=8, minute=0)
    scheduler.start()
    logger.info("✅ Scheduler iniciado com sucesso!")
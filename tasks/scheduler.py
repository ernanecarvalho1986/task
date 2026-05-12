import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from .models import Task
from .telegram import enviar_telegram

logger = logging.getLogger(__name__)

def verificar_tarefas():
    logger.info("🔔 Scheduler rodando — verificando tarefas...")
    hoje = date.today()
    tarefas = Task.objects.filter(data_limite=hoje, concluida=False).select_related('usuario__profile')
    logger.info(f"Tarefas encontradas para hoje: {tarefas.count()}")
    for t in tarefas:
        try:
            chat_id = t.usuario.profile.telegram_chat_id
            if chat_id:
                msg = f"⚠️ LEMBRETE: Tarefa '{t.titulo}' vence HOJE! Conclua agora."
                resultado = enviar_telegram(chat_id, msg)
                logger.info(f"Telegram enviado para {t.usuario.username} ({chat_id}): {resultado}")
            else:
                logger.info(f"Usuário {t.usuario.username} sem Telegram configurado, pulando.")
        except Exception as e:
            logger.error(f"Erro ao notificar {t.usuario.username}: {e}")

def start():
    logger.info("✅ Iniciando scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_tarefas, 'cron', hour=8, minute=0)
    scheduler.start()
    logger.info("✅ Scheduler iniciado com sucesso!")

import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def enviar_telegram(chat_id, mensagem):
    token = settings.TELEGRAM_BOT_TOKEN
    if not token or not chat_id:
        logger.warning("TELEGRAM_BOT_TOKEN ou chat_id ausente.")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={'chat_id': chat_id, 'text': mensagem}, timeout=10)
        if resp.status_code != 200:
            logger.error(f"Telegram API erro {resp.status_code}: {resp.text}")
        return resp.status_code == 200
    except Exception as e:
        logger.error(f"Erro ao enviar Telegram: {e}")
        return False

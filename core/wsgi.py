import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Inicia o scheduler após o Django carregar
try:
    from tasks.scheduler import start
    start()
except Exception as e:
    import logging
    logging.getLogger(__name__).error(f"Erro ao iniciar scheduler: {e}")
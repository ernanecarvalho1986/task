from django.apps import AppConfig

class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        import logging
        try:
            from . import scheduler
            scheduler.start()
        except Exception as e:
            logging.getLogger(__name__).error(f"Erro ao iniciar scheduler: {e}")
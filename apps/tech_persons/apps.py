from django.apps import AppConfig


class TechPersonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tech_persons'

    def ready(self):
        from apps.tech_persons import signals
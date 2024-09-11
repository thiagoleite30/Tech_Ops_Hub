from django.apps import AppConfig


class TechAssetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tech_assets'
    
    def ready(self):
        from apps.tech_assets import signals
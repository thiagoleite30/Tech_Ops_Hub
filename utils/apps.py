from django.apps import AppConfig
import os

class UtilsConfig(AppConfig):
    name = 'utils'
    path = os.path.join(os.path.dirname(__file__), 'utils')
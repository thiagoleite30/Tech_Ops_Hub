from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Sempre passando as configurações de ambiente default para o nosso projeto setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

# Criamos um app que recebera nosso servidor Celery
app = Celery('setup')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

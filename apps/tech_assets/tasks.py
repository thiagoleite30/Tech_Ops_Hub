from datetime import datetime
from celery import shared_task

from apps.tech_assets.models import Maintenance

@shared_task
def rotina_dias_atraso_manutencao():
    manutencoes = Maintenance.objects.filter(status=True)
    for manutencao in manutencoes:
        manutencao.dias_de_atraso()

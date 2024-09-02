from __future__ import absolute_import, unicode_literals
from sqlalchemy import create_engine
from celery import shared_task
import pandas as pd
from django.conf import settings

from apps.move_gpos.services import upload_gpos

@shared_task
def add():
    print(f"DEBUG :: CELERY :: TAREFA CHAMADA")
    
    

@shared_task
def consulta_bd_mv():
    engine = create_engine(settings.CONNETION_URL)
    with engine.connect() as connection:
        df_consulta = pd.read_sql_query(settings.SQL_QUERY_POS, connection)
    
    upload_gpos(df_consulta)
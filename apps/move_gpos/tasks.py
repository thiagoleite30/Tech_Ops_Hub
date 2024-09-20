from __future__ import absolute_import, unicode_literals
from datetime import datetime
from sqlalchemy import create_engine
from celery import shared_task
import pandas as pd
from django.conf import settings

from apps.move_gpos.services import upload_gpos, verifica_requisicoes

@shared_task
def rotina_checa_requisicoes():
    verifica_requisicoes()
    print(f'Executada rotina de checagem de requisições em: {datetime.now()}')
    
    

@shared_task
def consulta_bd_mv(**kwargs):
    pos_number = kwargs.pop('pos_number', None)
    engine = create_engine(settings.CONNETION_URL)
    with engine.connect() as connection:
        if pos_number == None:
            print(f'\n\nCONSULTA SEM ARGUMNETO! POS NUMBER {pos_number}')
            df_consulta = pd.read_sql_query(settings.SQL_QUERY_POS, connection)
        else:
            print(f'\n\nCONSULTA COM ARGUMNETO! POS NUMBER {pos_number}')
            df_consulta = pd.read_sql_query(f'{settings.SQL_QUERY_POS} AND CO.PosNumber = {pos_number}', connection)
    
    upload_gpos(df_consulta)
    print(f'Executada rotina de atualização de GPOS em: {datetime.now()}')
    
    
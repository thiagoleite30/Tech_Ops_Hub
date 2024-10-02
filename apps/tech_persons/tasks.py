from __future__ import absolute_import, unicode_literals
from datetime import datetime
from sqlalchemy import create_engine, text
from celery import shared_task
import pandas as pd
from django.conf import settings

from apps.tech_persons.services import upload_employee


@shared_task
def consulta_staging_tb_fp(**kwargs):
    engine = create_engine(f'oracle+cx_oracle://{settings.STAGING_USER}:{settings.STAGING_PASSWORD}@{settings.TNS_NAME}')
    sql_query_profile = """
                        SELECT SETOR, FILIAL, MATRICULA, NOME, CPF, CARGO, CENTRO_CUSTO, SITUACAO, SITUACAO_DATA_FIM FROM FP.TB_FP_PROTHEUS
                        UNION ALL
                        SELECT SETOR, FILIAL, MATRICULA, NOME, CPF, CARGO, CENTRO_CUSTO, SITUACAO, SITUACAO_DATA_FIM FROM FP.TB_FP_RM
                        """
    with engine.connect() as connection:
            df = pd.read_sql_query(
                text(sql_query_profile), connection)

    upload_employee(df)
    print(f'Executada rotina de atualização de GPOS em: {datetime.now()}')


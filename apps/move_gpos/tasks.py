from __future__ import absolute_import, unicode_literals
from datetime import datetime
import time
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
        if pos_number is None:
            df_consulta = pd.read_sql_query(settings.SQL_QUERY_POS, connection)
            print(f'\n\nCONSULTA SEM ARGUMNETO! POS NUMBER {pos_number}')
        else:
            query = """
                SELECT
                    CO.Id AS Id,
                    CO.Name AS ID_GPOS,
                    SH2.Name AS Loja,
                    SH.Name AS PDV,
                    CO.Description AS Description,
                    CO.MacAddress AS MacAddress,
                    CO.Active AS Active,
                    CO.PosNumber AS PosNumber,
                    CO.OnlyPreSales AS OnlyPreSales,
                    CO.IsDefaultComputer AS PrimaryPDV,
                    CO.CreationDate AS CreationDate,
                    CO.CreatorUser AS CreatorUser,
                    CO.LastUpdateDate AS LastUpdateDate,
                    CO.ComputerType AS ComputerType,
                    al.[DateTime] AS DATA_ULTIMO_LOGON,
                    us.UserName AS LastUserLogon,
                    us.Code AS Matricula
                FROM
                    MultiVendas.dbo.Computers CO
                    LEFT JOIN MultiVendas.dbo.AuditLogs AL
                        ON CO.Id = AL.Computer
                        AND AL.Id = (
                            SELECT MAX(a.Id)
                            FROM MultiVendas.dbo.AuditLogs a
                            WHERE a.Computer = CO.Id
                        )
                    LEFT JOIN MultiVendas.dbo.Users US
                        ON US.Id = AL.TargetUser
                    LEFT JOIN MultiVendas.dbo.Users US2
                        ON US2.Id = CO.CreatorUser
                    LEFT JOIN MultiVendas.dbo.Shops SH
                        ON SH.Id = CO.Shop
                    LEFT JOIN MultiVendas.dbo.Shops SH2
                        ON SH2.Id = SH.Parent
                WHERE
                    CO.ComputerType = 16
                    AND CO.PosNumber = ?
            """
            df_consulta = pd.read_sql_query(
                query, connection, params=(pos_number,))

    upload_gpos(df_consulta)
    print(f'Executada rotina de atualização de GPOS em: {datetime.now()}')


import time
from django.db import IntegrityError
from django.utils import timezone

from django.contrib import messages
import pandas as pd
import requests

from apps.tech_assets.models import Asset, AssetInfo, AssetModel, AssetType, Location, LogonInAsset, Manufacturer
from apps.move_gpos.models import GPOS, Request
from apps.move_gpos.TopDesk.TopDesk import TopDesk
from apps.tech_assets.services import register_logentry
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.conf import settings
from django.contrib.auth import get_user_model


def upload_gpos(df):
    # Filtrando apenas as linhas que possuem um endereço MAC válido
    df = df[df['MacAddress'].notna() & (df['MacAddress'] != '')]
    df.dropna(subset=['Loja', 'Id', 'MacAddress',
              'PosNumber', 'PDV'], inplace=True)
    for index, row in df.iterrows():
        tipo, created = AssetType.objects.get_or_create(nome='GPOS')

        fabricante, created = Manufacturer.objects.get_or_create(nome='Gertec')
        loja, created = Location.objects.get_or_create(nome=row['Loja'])
        pdv, created = Location.objects.update_or_create(
            nome=row['PDV'], defaults={'local_pai': loja})
        try:
            # Se não existir, crie o Asset o save() do asset já cria o AssetInfo
            ativo, _ = Asset.objects.update_or_create(
                nome=row['ID_GPOS'],
                defaults={
                    'numero_serie': row['MacAddress'],
                    'tipo': tipo,
                })

            if row['PrimaryPDV']:
                ativo.localizacao = pdv
                ativo.save()

            ativo_info = AssetInfo.objects.update_or_create(
                ativo=ativo,
                defaults={
                    'fabricante': fabricante,
                    'endereco_mac': row['MacAddress'],
                    'ultimo_logon': timezone.make_aware(row['DATA_ULTIMO_LOGON']) if not pd.isna(row['DATA_ULTIMO_LOGON']) else None,
                    'ultimo_scan': timezone.now()
                }
            )

            # Crie ou atualize o GPOS
            gpos, created = GPOS.objects.update_or_create(
                id=int(row['Id']),
                defaults={
                    'ativo': ativo,
                    'loja': loja,
                    'pdv': pdv,
                    'description': row['Description'],
                    'active': True if row['Active'] else False,
                    'pos_number': row['PosNumber'],
                    'only_pre_sales': row['OnlyPreSales'],
                    'primary_pdv': True if row['PrimaryPDV'] else False,
                    'creator_user': row['CreatorUser'],
                    'username_last_user_logon': row['LastUserLogon'],
                    'code_last_user_logon': row['Matricula'],
                    'last_logon_date': timezone.make_aware(row['DATA_ULTIMO_LOGON']) if not pd.isna(row['DATA_ULTIMO_LOGON']) else None,
                    'computer_type': row['ComputerType'],
                    'is_mac': True if ':' in row['MacAddress'] else False,
                    'blocked': True if Request.objects.filter(gpos__id=int(row['Id']), concluida=False).exists() else False
                }
            )

        except IntegrityError as e:
            # Ignora erros de integridade e continua o fluxo
            print(f"ERROR :: GPOS {row['ID_GPOS']} {e}")
        except Exception as e:
            print(f"ERROR :: GPOS {row['ID_GPOS']} {e}")


def dispara_fluxo_debug(request, json_request):
    print(
        f'Usuario: {request.user}\nEmail: {request.user.email}\nDisplayName: {request.user.first_name}')
    print(f'{json_request}')
    topdesk = TopDesk()

    query_call = topdesk.query_call_pos(json_request['posNumber'])
    print(f'Status Code POS {json_request["posNumber"]}: {query_call}')


def dispara_fluxo(request, json_request):
    topdesk = TopDesk()

    query_call = topdesk.query_call_pos(json_request['posNumber'])

    if query_call[0] == 200:
        messages.warning(
            request, f'Já existe um chamado aberto para mudança deste POS. Chamado: {query_call[1]}')
    elif query_call[0] == 204:
        response = topdesk.open_call(request.user.email, json_request['posNumber'], request.user.first_name,
                                     json_request['oldPDV'], json_request['newPDV'], json_request['posIMEI'])
        if response[0] == 201:
            json_request['chamado'] = response[1]
            response_pa = requests.post(settings.URL_FLOW, json=json_request)

            if response_pa.status_code == 202:
                messages.success(request, f"""Sua solicitação foi inserida na fila e gerou o chamado {
                    response[1]}."""
                                 )
            else:
                topdesk.put_action(
                    response[1], response_pa.status_code)
                messages.error(request, f"""ATENÇÃO: Sua solicitação gerou o chamado {
                    response[1]}. No entanto, ocorreu um erro ao inserir na fila de troca(CODE: {response_pa.status_code})."""
                               )
        else:
            messages.error(request, f"""Algo deu errado na abertura de nova solicitação. Contate o suporte! Status code: {
                response[0]}""")
        return response
    else:
        messages.error(request, f"""Ocorreu um erro ao processar a buscar por um chamado referente ao POS {
            json_request['posNumber']}. Contate o suporte.\nO Status code é: {query_call[0]}"""
                       )
    return None


def verifica_requisicoes():

    topdesk = TopDesk()

    requisicoes = Request.objects.filter(concluida=False)

    for requisicao in requisicoes:
        if requisicao.chamado != None:
            if topdesk.get_status_call(requisicao.chamado):
                from apps.move_gpos.tasks import consulta_bd_mv
                requisicao.concluida = True
                requisicao.data_conclusao = timezone.now()
                consulta_bd_mv(pos_number=requisicao.gpos.pos_number)
                requisicao.save()

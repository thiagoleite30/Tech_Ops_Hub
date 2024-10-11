import os
import base64
import requests
import pandas as pd
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, \
      CHANGE
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model




from apps.tech_assets.models import Asset, AssetInfo, AssetModel, \
      AssetType, LogonInAsset, Movement, Maintenance, Manufacturer



def register_logentry(instance, action, **kwargs):
    usuario = kwargs.get('user', None)
    print(f'DEBUG :: SERVICE :: REGISTER LOG ENTRY :: {usuario}')
    content_type = ContentType.objects.get_for_model(instance)
    object_id = instance.pk
    if action == ADDITION:
        details = f"""O objeto {content_type.model} ID '{
            instance.pk}' foi criada pelo usuário {usuario}"""
        if kwargs.get('detalhe', None) != None:
            detalhe = kwargs.get('detalhe', None)
            str.join(details, f' {detalhe}')

        details = f"""O objeto {content_type.model} ID '{
            instance.pk}' foi criada pelo usuário {usuario}"""
    elif action == CHANGE:
        details = f"""O objeto {content_type.model} ID '{
            instance.pk}' foi modificado pelo usuário {usuario}"""
        if kwargs.get('modificacao', None) != None:
            modificacao = kwargs.get('modificacao', None)
            str.join(details, f' {modificacao}')
    else:
        object_id = kwargs.get('foto_id', None)
        details = f"""O objeto {content_type.model} ID '{
            instance.pk}' foi deletado pelo usuário {usuario}"""
        if kwargs.get('detalhe', None) != None:
            detalhe = kwargs.get('detalhe', None)
            str.join(details, f' {detalhe}')

    # Salvar no log
    LogEntry.objects.create(
        user=usuario,
        content_type=content_type,
        object_id=object_id,
        object_repr=str(instance),
        action_flag=action,
        change_message=details
    )


def get_user_photo_microsoft(user):
    try:
        social_account = SocialAccount.objects.get(
            user=user, provider='microsoft')

        # print(f"DEBUG :: SERVICES :: USER = {social_account}")

        social_token = SocialToken.objects.get(
            account_id=social_account.id).token

        # print(f"DEBUG :: SERVICES :: TOKEN = {social_token}")

        headers = {
            'Authorization': 'Bearer ' + social_token
        }
        graph_api_url = 'https://graph.microsoft.com/v1.0/me/photo/$value'
        response = requests.get(graph_api_url, headers=headers)

        if response.status_code == 200:
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64  # Retornar a foto
        else:
            return None
    # Caso o usuário logado não seja um login social, ou seja, um usuário criado em admin ou superusuario
    except SocialAccount.DoesNotExist as erro:
        # print(f"ERROR :: SERVICES :: SOCIAL ACCOUNT ERROR = {erro}")
        return None


def get_employedId(user):
    try:
        social_account = SocialAccount.objects.get(
            user=user, provider='microsoft')

        # print(f"DEBUG :: SERVICES :: USER = {social_account}")

        social_token = SocialToken.objects.get(
            account_id=social_account.id).token

        headers = {
            'Authorization': 'Bearer ' + social_token
        }
        employedId = requests.get(
            f'https://graph.microsoft.com/beta/users/{user.email}', headers=headers)

        if employedId.status_code == 200:
            return employedId.json()["employeeId"]
        else:
            return None
    # Caso o usuário logado não seja um login social, ou seja, um usuário criado em admin ou superusuario
    except SocialAccount.DoesNotExist as erro:
        # print(f"ERROR :: SERVICES :: SOCIAL ACCOUNT ERROR = {erro}")
        return None


# Retorna status de não disponível igual False, ou seja,
    # sem empréstimo, e o queryset, em caso de não exisir empréstimo ativo será vazio
def get_movement_asset(asset_id):

    status_ativos = [
        'pendente_aprovacao',
        'em_andamento',
        'atrasado'
    ]
    return {'status': Movement.objects.filter(status__in=status_ativos, ativos__id=asset_id).exists(),
            'queryset': Movement.objects.filter(status__in=status_ativos,
                                                ativos__id=asset_id),
            'list_status': [movimento.status for movimento in Movement.objects.filter(status__in=status_ativos,
                                                                                      ativos__id=asset_id)]}


def get_maintenance_asset(asset_id):  # Busca manutencia de um asset

    return {'status': Maintenance.objects.filter(status=True, ativo=asset_id).exists(),
            'queryset': Maintenance.objects.filter(status=True, ativo=asset_id)}


def get_movement_status_pendente(asset_id):
    return Movement.objects.filter(ativos=asset_id, status__in=['pendente_aprovacao']).exists()


def concluir_manutencao_service(asset_id, user):
    asset = get_object_or_404(Asset, id=asset_id)
    if asset:
        if Maintenance.objects.filter(ativo=asset, status=True).exists():
            maintenance = get_object_or_404(
                Maintenance, ativo=asset, status=True)
            Maintenance.marcar_como_finalizada(maintenance)
            modificacao = f'''Alterou status para "False" (Não ativa)'''
            register_logentry(instance=maintenance, action=CHANGE,
                              modificacao=modificacao, user=user)

        movement_exist = get_movement_asset(asset_id)
        if movement_exist['status']:
            if 'pendente_aprovacao' in movement_exist['list_status']:
                asset.status = 'separado'
                asset.save()
                modificacao = f'Alterou status para "Separado"'
            elif 'em_andamento' in movement_exist['list_status'] or 'atrasado' in movement_exist['list_status']:
                asset.status = 'em_uso'
                asset.save()
                modificacao = f'Alterou status para "Em Uso"'
        else:
            asset.status = 'em_estoque'
            asset.save()
            modificacao = f'Alterou status para "Em Estoque"'
            register_logentry(instance=asset, action=CHANGE,
                              modificacao=modificacao, user=user)
        return True
    return False


def upload_assets(csv_file):
    df = pd.read_csv(csv_file, sep=';')
    df = df[df['numero_serie'].notna() & (df['numero_serie'] != '')]
    df.dropna(subset=['numero_serie', 'nome', 'tipo', 'modelo'], inplace=True)
    filtered_df = df[df['nome'].str.match(r'(?i)^(RQR|CDS|RQE)')]
    df = filtered_df.reset_index(drop=True)
    try:
        # Processamento das datas
        df['data_instalacao_so'] = pd.to_datetime(df['data_instalacao_so'], format='%m/%d/%Y %I:%M:%S %p %z', errors='coerce', utc=True)
        df['data_instalacao_so'] = df['data_instalacao_so'].dt.tz_convert('America/Sao_Paulo')
        df['data_garantia'] = pd.to_datetime(df['data_garantia'], format='%m/%d/%Y %I:%M:%S %p %z', errors='coerce', utc=True)
        df['data_garantia'] = df['data_garantia'].dt.tz_convert('America/Sao_Paulo')
        df['ultimo_logon'] = pd.to_datetime(df['ultimo_logon'], format='%m/%d/%Y %I:%M:%S %p %z', errors='coerce', utc=True)
        df['ultimo_logon'] = df['ultimo_logon'].dt.tz_convert('America/Sao_Paulo')
        df['ultimo_scan'] = pd.to_datetime(df['ultimo_scan'], format='%d/%m/%Y %I:%M:%S', errors='coerce', utc=False)
        df['ultimo_scan'] = df['ultimo_scan'].dt.tz_convert('America/Sao_Paulo')
    except Exception as e:
        print(f'Erro ao converter informações de data!')

    # Criando os assets, assetinfo, modelo, tipos e fabricantes
    for index, row in df.iterrows():
        tipo, _ = AssetType.objects.get_or_create(nome=row['tipo'])

        fabricante, _ = Manufacturer.objects.get_or_create(nome=row['fabricante'])

        modelo, _ = AssetModel.objects.update_or_create(nome=row['modelo'], defaults={'tipo': tipo, 'fabricante': fabricante})

        # Criando os objetos Asset e AssetInfo, tipos e fabricantes
        try:
            ativo, _ = Asset.objects.update_or_create(
                numero_serie=row['numero_serie'],
                defaults={
                    'nome': row['nome'],
                    'tipo': tipo,
                    'modelo': modelo,
                }
            )

            ativo_info, _ = AssetInfo.objects.update_or_create(
                ativo=ativo,
                defaults={
                    'fabricante': fabricante,
                    'memoria': row['memoria'],
                    'armazenamento': row['armazenamento'],
                    'processador': row['processador'],
                    'plataforma': row['so'],
                    'versao_plataforma': row['versao_so'],
                    'licenca_plataforma': row['licenca_so'],
                    'data_instalacao_plataforma': row['data_instalacao_so'] if not pd.isna(row['data_instalacao_so']) else None,
                    'data_garantia': row['data_garantia'] if not pd.isna(row['data_garantia']) else None,
                    'endereco_mac': row['endereco_mac'],
                    'ultimo_logon': row['ultimo_logon'] if not pd.isna(row['ultimo_logon']) else None,
                    'ultimo_scan': row['ultimo_scan'] if not pd.isna(row['ultimo_scan']) else None
                }
            )

            User = get_user_model()

            if User.objects.filter(username=row['username']).exists():
                user_logon = User.objects.get(username=row['username'])
            else:
                user_logon = None


            logon_in_asset, created = LogonInAsset.objects.get_or_create(
                ativo=ativo,
                data_logon=ativo_info.ultimo_logon,
                defaults={
                    'user': user_logon,
                    'user_name': row['username'],
                    'data_logon': ativo_info.ultimo_logon if ativo_info.ultimo_logon else None,
                }
            )

        except IntegrityError as e:
            # Ignora o erro e continua o fluxo
            print(f"""Erro ao criar o tipo '{row['modelo']}': {e}""")
        except Exception as e:
            print(f"""Erro inesperado ao processar '{
                  row['modelo']}' ativo {ativo.id}: {e}""")


def read_file():
    full_path = os.path.join(r'\\10.94.1.49\Thiago',r'web50repecef7965a477415281b850050f8b6615 (5).csv')
    df = pd.read_csv(full_path, sep=';')
    print(df)
from datetime import timezone
from django.db import IntegrityError
import pandas as pd

from apps.tech_assets.models import Asset, AssetInfo, AssetModel, AssetType, Location, Manufacturer
from apps.move_gpos.models import GPOS
from apps.tech_assets.services import register_logentry
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

def upload_gpos(df):
    # Filtrando apenas as linhas que possuem um endereço MAC válido
    df = df[df['MacAddress'].notna() & (df['MacAddress'] != '')]

    for index, row in df.iterrows():
        tipo, created = AssetType.objects.get_or_create(nome='GPOS')
        
        fabricante, created = Manufacturer.objects.get_or_create(nome='Gertec')
        
        loja, created = Location.objects.get_or_create(nome=row['Loja'])
        
        pdv, created = Location.objects.update_or_create(nome=row['PDV'], defaults={
            'local_pai':loja})

        try:
            # Verifique se o AssetInfo já existe com o endereço MAC
            if AssetInfo.objects.filter(endereco_mac=row['MacAddress']).exists():
                ativo_info = AssetInfo.objects.get(endereco_mac=row['MacAddress'])
                ativo = ativo_info.ativo
            else:
                # Se não existir, crie o Asset e o AssetInfo
                ativo, created = Asset.objects.update_or_create(
                    nome=row['ID_GPOS'],
                    defaults={
                        'numero_serie':row['MacAddress'],
                        'tipo':tipo,
                    }

                )
                if row['PrimaryPDV']:
                    ativo.localizacao = pdv
                    ativo.save()

                if created:
                    # Criar AssetInfo
                    ativo_info = AssetInfo.objects.create(
                        ativo=ativo,
                        fabricante=fabricante,
                        endereco_mac=row['MacAddress'],
                    )
                
            
            print(f'DEBUG :: GET OR CREATE GPOS :: AGORA VAI CRIAR O GPOS ID {row['ID_GPOS']}...')
            # Crie ou atualize o GPOS
            gpos, created = GPOS.objects.update_or_create(
                id=int(row['Id']),
                defaults={
                    'ativo': ativo,
                    'loja': loja,
                    'pdv': pdv,
                    'description': row['Description'],
                    'active': row['Active'],
                    'pos_number': row['PosNumber'],
                    'only_pre_sales': row['OnlyPreSales'],
                    'primary_pdv': row['PrimaryPDV'],
                    'creator_user': row['CreatorUser'],
                    'computer_type': row['ComputerType'],
                }
            )
            
            if created:
                print(f'DEBUG :: CREATE GPOS :: CRIOU O GPOS ID {gpos.id} {row['ID_GPOS']}...')
            else:
                print(f'DEBUG :: CREATE GPOS :: SOMENTE PEGOU O GPOS {gpos.id}  {row['ID_GPOS']}...')
        
        except IntegrityError as e:
            # Ignora erros de integridade e continua o fluxo
            print(f"ERROR :: GPOS {row['ID_GPOS']} {e}")
        except Exception as e:
            print(f"ERROR :: GPOS {row['ID_GPOS']} {e}")
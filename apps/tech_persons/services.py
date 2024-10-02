import pandas as pd
from django.db import IntegrityError
from django.utils import timezone

from apps.tech_persons.models import *


def upload_employee(df):
    try:
        df = df[(df['cpf'].notna()) & (df['cpf'] != '')]
        df['situacao_data_fim'] = pd.to_datetime(df['situacao_data_fim'], format='%d/%m/%Y', errors='coerce')
        df_resultado = df.sort_values(by=['cpf', 'situacao_data_fim']).drop_duplicates(subset='cpf', keep='last', ignore_index=True)
        df_resultado.reset_index(drop=True,inplace=True)

        for index, row in df_resultado.iterrows():
            cc = CostCenter.objects.filter(nome__iexact=row['centro_custo']).first()
            if not cc:
                cc = CostCenter.objects.create(nome=row['centro_custo'])
                print(f'Centro de custo criado: {cc}')
            
            employee , created = Employee.objects.update_or_create(
                cpf=row['cpf'],
                defaults={
                    'setor': row['setor'],
                    'filial': row['filial'],
                    'matricula': row['matricula'],
                    'nome': row['nome'],
                    'cargo': row['cargo'],
                    'centro_custo': cc,
                    'situacao': row['situacao'],
                    'situacao_data_fim': timezone.make_aware(row['situacao_data_fim']) if not pd.isna(row['situacao_data_fim']) else None,
                }
            )

            if created:
                print(f'\nDEBUG :: CREATE EMPLOYEE {employee}')
                
            employee.save()
    
    except IntegrityError as e:
        print(f'\nERROR :: EMPLOYEE {e}')

    except Exception as e:
         print(f'\nERROR :: EMPLOYEE {e}')
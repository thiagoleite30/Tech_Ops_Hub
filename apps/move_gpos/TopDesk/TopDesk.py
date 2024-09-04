import base64
from uu import Error
import requests
from django.conf import settings

from sqlalchemy import true


class TopDesk:
    def __init__(self) -> None:
        self._token_utf8 = (f"{settings.USER_TOPDESK}:{settings.KEY_TOPDESK}").encode('utf-8')
        self._credpair = base64.b64encode(self._token_utf8).decode('utf-8')
        self._headers = {'Authorization': 'Basic {}'.format(self._credpair)}


    def open_call(self, email, posnumber, dynamicName, oldpdv, newpdv, imei):
        try:
            json = {
            'caller' : {'id' : self.get_id_caller(email)},
            'callType' : {'name' : 'Requisição'},
            'priority' : {'name' : 'Requisição - Baixa'},
            'sla' : {'id': '3515ac19-31be-4306-a932-997fb40f81e9'},
            'briefDescription': f'Movimentação do {posnumber}',
            'optionalFields2': {'boolean2': True, 'text5': f'{posnumber}'},
            'category' : {'name' : 'Multivendas - GPOS'},
            'subcategory' : {'name' : 'Mudar PDV'},
            'entryType' : {'name' : 'Rôbo Service Desk'},
            'impact': {'id': '6dd9cf42-0529-52bc-bbee-87872646ac71'},
            'urgency': {'id': '38548ee9-53a0-4458-a22d-bdb3fa4121ea'},
            'operator': {'id': 'e1936b2b-4f3d-4549-97bf-17ef26fa5070'},
            'operatorGroup': {'id': '5eb97f94-0831-47e9-bf0c-a2f8a85e7c60'},
            'request' : f'<b>{dynamicName}</b></br><b>Alterar o GPOS:</b></br><b>Número do POS: </b>{posnumber}</br><b>IMEI/MAC: </b>{imei}</br><b>PDV Atual: </b>{oldpdv}</br><b>Novo PDV: </b>{newpdv}'
            
            }
            response = requests.post(f'{settings.API_TOPDESK_URL}/incidents', json=json, headers=self._headers)
            if response.status_code == 201:
                #logger_topdesk.info(f"Conexão com a API estabelecida com sucesso. Chamado {response.json()['number']} aberto!")
                return response.status_code, response.json()['number']
            else:
                #logger_topdesk.info(f"Algo deu errado na abertura do chamado. Status Code: {response.status_code}")
                return response.status_code, f"Erro ao abrir chamado! Status code: {response.status_code}"
        except Error as e:
            #logger_topdesk.error("Erro ao conectar com a API TopDesk: %s", e)
            print("Erro ao conectar com a API TopDesk. Verifique o log para mais detalhes.")


    def get_id_caller(self, email):
        try:
            response = requests.get(f'{settings.API_TOPDESK_URL}/persons?page_size=1&query=email=="{email}"', headers=self._headers)
            if response.status_code == 200 or response.status_code == 206:
                #logger_topdesk.info(f"GET ID CALLER :: Localizado o id caller. Status Code: {response.status_code}")
                return response.json()[0]['id']
            else:
                #logger_topdesk.info(f"GET ID CALLER :: Algo deu errado na busca pelo id caller. Status Code: {response.status_code}")
                return 'ac9defc9-fa99-4351-b285-02e96f68337d'
        except Error as e:
            #logger_topdesk.error("Erro ao conectar com a API TopDesk: %s", e)
            print("Erro ao conectar com a API TopDesk. Verifique o log para mais detalhes.")
    
    def query_call_pos(self, posnumber):
        #print(f'O QueryCall recebeu: {posnumber}')
        try:
            #pos = "POS " + str(posnumber)
            #print(f'\n{settings.API_TOPDESK_URL}/incidents?&query=completed==False;briefDescription=="POS {posnumber}";(processingStatus.name!="Resolvido",processingStatus.name!="Fechado")')
            #response = requests.get(f'{settings.API_TOPDESK_URL}/incidents?&query=completed==False;briefDescription=="{posnumber}";(processingStatus.name!="Resolvido",processingStatus.name!="Fechado")', headers=self._headers)
            response = requests.get(f'{settings.API_TOPDESK_URL}/incidents?&query=completed==False;optionalFields2.text5=="{posnumber}";(processingStatus.name!="Resolvido",processingStatus.name!="Fechado")', headers=self._headers)
            if response.status_code == 200:
                #logger_topdesk.info(f"QUERY CALL POS :: Localizado Chamado {response.json()[0]['number']}. Status Code: {response.status_code}")
                return response.status_code, response.json()[0]['number']
            elif response.status_code == 204:
                #logger_topdesk.info(f"QUERY CALL POS :: Não localizado nenhum chamado pendente para POS {posnumber}. Status Code: {response.status_code}")
                return response.status_code, f'Status Code: {response.status_code}'
            else:
                #logger_topdesk.info(f"QUERY CALL POS :: Algo deu errado na query. Status Code: {response.status_code}")
                return response.status_code, f'Status Code: {response.status_code}'
        except Error as e:
            #logger_topdesk.error("Erro ao conectar com a API TopDesk: %s", e)
            print("Erro ao conectar com a API TopDesk. Verifique o log para mais detalhes.")

    def put_action(self, call_number, status_code):
        try:
           json = {
                    "action": f"<b>ATENÇÃO!</b></br>Ocorreu um erro ao enfileirar a solicitação no fluxo.</br><b>Código reportado: {status_code}<b/>",
                    "processingStatus": {
                        "name": "Respondido pelo usuário"
                    },
                    "actionInvisibleForCaller": False,
                    "completed": False,
                    }
           response = requests.put(f'{settings.API_TOPDESK_URL}/incidents/number/{call_number}', headers=self._headers, json=json)
        except Error as e:
            #logger_topdesk.error("Erro ao conectar com a API TopDesk: %s", e)
            print("Erro ao conectar com a API TopDesk. Verifique o log para mais detalhes.")

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
import requests
from allauth.socialaccount.models import SocialAccount, SocialToken
import base64

def register_logentry(instance, action, **kwargs):
    usuario=kwargs.get('user', None)
    print(f'DEBUG :: SERVICE :: REGISTER LOG ENTRY :: {usuario}')
    content_type = ContentType.objects.get_for_model(instance)
    object_id=instance.pk
    if action == ADDITION:
        details = f"O objeto {content_type.model} ID '{instance.pk}' foi criada pelo usuário {usuario}"
    elif action == CHANGE:
        details = f"O objeto {content_type.model} ID '{instance.pk}' foi modificado pelo usuário {usuario}"
    else:
        object_id=kwargs.get('foto_id', None)
        details = f"O objeto {content_type.model} ID '{instance.pk}' foi deletado pelo usuário {usuario}"

    print(details)
    print(f'DEBUG :: SERVICE :: REGISTER LOG ENTRY :: content_type {content_type}')
    print(f'DEBUG :: SERVICE :: REGISTER LOG ENTRY :: object_id {object_id}')
    print(f'DEBUG :: SERVICE :: REGISTER LOG ENTRY :: object_repr {str(instance)}')
    print(f'DEBUG :: SERVICE :: REGISTER LOG ENTRY :: action_flag {action}')
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
        social_account = SocialAccount.objects.get(user=user, provider='microsoft')
        
        #print(f"DEBUG :: SERVICES :: USER = {social_account}")
        
        social_token = SocialToken.objects.get(account_id=social_account.id).token
        
        #print(f"DEBUG :: SERVICES :: TOKEN = {social_token}")
        
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
    except SocialAccount.DoesNotExist as erro: # Caso o usuário logado não seja um login social, ou seja, um usuário criado em admin ou superusuario
        #print(f"ERROR :: SERVICES :: SOCIAL ACCOUNT ERROR = {erro}")
        return None
import string
from allauth.account.models import EmailAddress
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import requests
from allauth.socialaccount.models import SocialAccount, SocialToken
from apps.tech_assets.services import get_employedId
from apps.tech_persons.models import UserEmployee


class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form):
        print(f'DEBUG :: ENTROU NO SAVE USER DO ADAPTER :: USER {user}')

        email = form.cleaned_data.get('email')
        User = get_user_model()
        # Verifica se o e-mail já existe no banco de dados
        if User.objects.filter(email=email).exists():
            as_user = User.objects.get(email=email)
            return as_user
        # Se não tiver usuário com email então cria um novo com as informações do login social
        user = super().save_user(request, user, form, commit=False)
        user.email = email
        user.save()

        return user
    
"""
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('mail')
        print(f'DEBUG :: ENTROU NO PRE SOCIAL LOGIN DO ADAPTER :: EMAIL {email}')
        #print(f'DEBUG :: extra_data: {sociallogin.account.extra_data}')
        if email:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                request.session['type_login'] = 'social' # Aqui defini um valor pra sessão de tipo para que no logout seja redirecionado pra URL correta
            except User.DoesNotExist:
                pass
"""

# O Adapter acima foi modificado aqui para fazer vinculo entre usuário e conta social \
#  pela exitencia de um UserEmployee (vinculo entre associado e usuário)
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('mail')
        access_token = sociallogin.token.token

        if access_token:
            headers = {
                'Authorization': 'Bearer ' + access_token
            }
            try:
                employedId = requests.get(
                    f'https://graph.microsoft.com/beta/users/{email}', headers=headers).json()["employeeId"]
                print(f'DEBUG :: EmployeedId {employedId}')
                filial, matricula = employedId.split('_')
                print(f'\nDEBUG :: FILIAL {filial} :: MATRICULA {matricula}')
                if UserEmployee.objects.filter(employee__filial=filial, employee__matricula=matricula).exists():
                    user_filter = UserEmployee.objects.filter(employee__filial=filial, employee__matricula=matricula).first()
                    usuario = user_filter.user
                    sociallogin.connect(request, usuario)
                    request.session['type_login'] = 'social' # Aqui defini um valor pra sessão de tipo para que no logout seja redirecionado pra URL correta
                    email, created = EmailAddress.objects.get_or_create(user=usuario, email=email, verified=False, primary=True)
                    if not usuario.email:
                        print(f'\nDEBUG :: USUARIO TEM INFORMAÇÃO DE EMAIL VAZIA!')
                        usuario.email = str(email)
                        usuario.save()
                    print(f'\n\nDEBUG :: ENCONTRADO USARIO/ASSOCIADO :: {user_filter.user} {user_filter.employee}')
                else:
                    print(f'\n\nDEBUG :: USUARIO/ASSOCIADO NÃO LOCALIZADO COM EMPLOYEEID {employedId}')
                    raise Exception('Usuário não encontrado para o Employee ID fornecido')

            except Exception as e:
                print(f'ERROR :: {e}')



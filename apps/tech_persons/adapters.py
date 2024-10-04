from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

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

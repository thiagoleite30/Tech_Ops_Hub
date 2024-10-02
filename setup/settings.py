"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from sqlalchemy.engine import URL
from pathlib import Path, os
from dotenv import load_dotenv

# Carregando variáveis de ambiente
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.94.1.49', 'localhost',
                 '127.0.0.1', 'techopshub-test.aviva.com.br']

# Definindo o caminho/registro da aplicação
# Por ser desenvolvimento então

SITE_ID = 1


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

LOCAL_APPS = [
    'apps.move_gpos.apps.MoveGposConfig',
    'apps.tech_assets.apps.TechAssetsConfig',
    'apps.tech_persons.apps.TechPersonsConfig',
    'utils.apps.UtilsConfig',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft',
    'pwa',
    'debug_toolbar',
    'django_filters',
]


INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.tech_assets.context_processors_add.cart_item_count',
                'apps.tech_assets.context_processors_add.verifica_aprovacoes_pendentes',
                'apps.tech_assets.context_processors_add.get_profile_info',
                'apps.tech_assets.context_processors_add.get_url_login_ms',
                'apps.tech_assets.context_processors_add.get_url_logout',
                'apps.tech_assets.context_processors_add.user_groups_processor',
                # 'apps.tech_assets.context_processors_add.is_administradores_user',
                # 'apps.tech_assets.context_processors_add.is_aprovadores_ti_user',
                # 'apps.tech_assets.context_processors_add.is_suporte_user',
                # 'apps.tech_assets.context_processors_add.is_mvgpos_user',
            ],



        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        # ou 'django.db.backends.sqlite3', 'django.db.backends.mysql', etc.
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.getenv('POSTGRES_DATABASE')),
        'USER': str(os.getenv('POSTGRES_USER')),
        'PASSWORD': str(os.getenv('POSTGRES_PASSWORD')),
        # ou o IP/hostname do servidor de banco de dados
        'HOST': str(os.getenv('POSTGRES_HOST')),
        # o número da porta, se não for o padrão
        'PORT': str(os.getenv('POSTGRES_PORT')),
        # conexão permanece aberta por 10 minutos
        # 'CONN_MAX_AGE': 600,
    }
}

# Configurações Staging

TNS_NAME=str(os.getenv('TNS_NAME'))
STAGING_USER=str(os.getenv('STAGING_USER'))
STAGING_PASSWORD=str(os.getenv('STAGING_PASSWORD'))


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'setup/static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações API Graphs

CLIENT_ID = str(os.getenv('CLIENT_ID'))
CLIENT_SECRET = str(os.getenv('CLIENT_SECRET'))
AUTHORITY = str(os.getenv('AUTHORITY'))

# Allauth e configurações especificas do provedor microsoft

SOCIALACCOUNT_PROVIDERS = {
    "microsoft": {
        "APPS": [
            {
                "client_id": str(os.getenv('CLIENT_ID')),
                "secret": str(os.getenv('CLIENT_SECRET')),
                "settings": {
                    "tenant": str(os.getenv('TENANT_ID')),
                    # Optional: override URLs (use base URLs without path)
                    # "login_url": "https://login.microsoftonline.com",
                    # "graph_url": "https://graph.microsoft.com",
                }
            }
        ],
        # 'REDIRECT_URI': 'http://localhost:8000/accounts/microsoft/login/callback/',
    }
}

SOCIALACCOUNT_STORE_TOKENS = True  # Para que o model guarde o social token

LOGIN_URL = str(os.getenv('URL_REDIRECT_POSLOGOUT'))

LOGIN_REDIRECT_URL = '/'  # ou a URL para onde deseja redirecionar após o login

# Altera o comportamento de, após login social do provedor, ir para uma tela padrão do Allauth. Vai direto pro URL definido acima
SOCIALACCOUNT_LOGIN_ON_GET = True

# Altera o comportamento de, após clicar no logout, ou digitar a URL de logout, ele não manda para uma página que pergunta se quero mesmo sair
ACCOUNT_LOGOUT_ON_GET = True

# ou a URL para onde deseja redirecionar após o logout - aqui tá indo pra index
LOGOUT_REDIRECT_URL = f'''https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri={LOGIN_URL}'''

URL_POS_CLICK_MS_LOGO = str(os.getenv('URL_POS_CLICK_MS_LOGO'))

# PWA Settings

PWA_APP_NAME = 'Tech Ops Hub'
PWA_APP_DESCRIPTION = "Hub de Operações Tecnológicas"
PWA_APP_THEME_COLOR = '#000'
PWA_APP_BACKGROUND_COLOR = '#fff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/assets/ícones/android-icons/android-launchericon-144-144.png',
        'sizes': '144x144'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/assets/ícones/ios-icons/144.png',
        'sizes': '144x144'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/assets/ícones/android-icons/android-launchericon-512-512.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'pt-br'

PWA_OFFLINE_URL = os.path.join(BASE_DIR, 'templates/shared/offline.html')


# Setting DB MV


CONNETION_STRING = f'''DRIVER={{{str(os.getenv("DRIVER"))}}};SERVER={str(os.getenv("HOST_DB_MV"))};DATABASE={str(os.getenv("DB_MV"))};Trusted_Connection=yes;'''

CONNETION_URL = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": CONNETION_STRING}
)

SQL_QUERY_POS = """SELECT 
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
    CO.ComputerType = 16SELECT 
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
    CO.ComputerType = 16"""


# Configuração TopDesk

API_TOPDESK_URL = str(os.getenv('API_TOPDESK_URL'))
USER_TOPDESK = str(os.getenv('USER_TOPDESK'))
KEY_TOPDESK = str(os.getenv('KEY_TOPDESK'))


# URL FLOW

URL_FLOW = str(os.getenv('URL_FLOW'))


# CELERY_BROKER_URL = 'amqp://toh:boils2020@localhost:5672'
CELERY_BROKER_URL = str(os.getenv('RMQ_URL'))

# Settings Schedule Celery

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'rodar_consulta_bd_mv': {
        'task': 'apps.move_gpos.tasks.consulta_bd_mv',
        'schedule': crontab(minute='*/30'),  # Executa a cada 30 minutos
    },
    'rodar_rotina_checa_requisicoes': {
        'task': 'apps.move_gpos.tasks.rotina_checa_requisicoes',
        'schedule': crontab(minute='*/5'),  # Executa a cada 20 minutos
    },
    'rodar_consulta_staging_tb_fp': {
        'task': 'apps.tech_persons.tasks.consulta_staging_tb_fp',
        'schedule': crontab(minute=0, hour='*/3'),  # Execute a cada três horas: meia-noite,
    },
}


# Configurar Internals IPs

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]
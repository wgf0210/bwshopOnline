import os,sys,datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zbxgue_5$-3(fux_ne4+clo!ki9jm0kwn26(*83b27o8*0tg6e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE':5,
    'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

# 登录方式自定义的配置
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',  # 手机号也可登录
    'social_core.backends.weibo.WeiboOAuth2',  # 第三方登录-微博
    'social_core.backends.weixin.WeixinOAuth2',  # 第三方登录-微信
    'social_core.backends.qq.QQOAuth2',  # 第三方登录-QQ
    'django.contrib.auth.backends.ModelBackend',
)

# 有效时期
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),    #也可设置seconds=20
    'JWT_AUTH_HEADER_PREFIX': 'JWT',   #JWT跟前端保持一致，
}

# 忽略最后的/
APPEND_SLASH=False

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 云片网 api_key
APIKEY = '0ae5e2675301de929b01be9c62630bdc'

# 重载系统的用户，让UserProfile生效
AUTH_USER_MODEL = 'users.UserProfile'

# 解决跨域问题
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'goods.apps.GoodsConfig',
    'trade.apps.GradeConfig',
    'user_operation.apps.UserOperationConfig',
    'xadmin',
    'reversion',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'DjangoUeditor',
    'django_filters',
    'coreschema',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'bwshopOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            #     第三方登录
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'bwshopOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'bwshoponline_db',
        'USER': 'root',
        'PASSWORD': "002598",
        'HOST': "127.0.0.1",
        # 'PASSWORD': "123456",
        # 'HOST': "39.107.141.56",
        'OPTIONS': { 'init_command': 'SET default_storage_engine=INNODB;' }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# 上传图片的文件夹
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 支付宝配置
private_key_path = os.path.join(BASE_DIR,'apps/trade/keys/应用私钥2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR,'apps/trade/keys/alipay_key_2048.txt')


'''
    第三方的登录配置
'''
# 微博
SOCIAL_AUTH_WEIBO_KEY = '1200417273'
SOCIAL_AUTH_WEIBO_SECRET = 'db3b028edc1688eef3f939f61e3d58c5'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'

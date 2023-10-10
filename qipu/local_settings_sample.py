SECRET_KEY = 'django-insecure-9xib+ljr(a2*@s$@902p-@3zbk_x1uf&*c%%-hy=wp&p5f-=r!'

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qipu_challenge',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'

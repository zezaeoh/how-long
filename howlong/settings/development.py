from .base import *

import json

DEBUG = True
ALLOWED_HOSTS = '*'

ENV_CONFIG_FILE = os.path.join(BASE_DIR, 'settings/env_development.json')
ENV_CONFIG = json.loads(open(ENV_CONFIG_FILE).read())
print('loading: env_development.json')

# MEDIA_URL = 'http://127.0.0.1:8000/'
# MEDIA_ROOT = '/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = ENV_CONFIG['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = ENV_CONFIG['aws']['secret_access_key_id']
AWS_STORAGE_BUCKET_NAME = ENV_CONFIG['aws']['storage_bucket_name']
AWS_S3_REGION_NAME = ENV_CONFIG['aws']['s3_region_name']
AWS_QUERYSTRING_AUTH = False

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ENV_CONFIG['database']['name'],
        'USER': ENV_CONFIG['database']['user'],
        'PASSWORD': ENV_CONFIG['database']['password'],
        'HOST': ENV_CONFIG['database']['host'],
        'PORT': ENV_CONFIG['database']['port'],
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    },
}
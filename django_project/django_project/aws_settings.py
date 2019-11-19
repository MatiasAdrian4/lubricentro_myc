from django_project.settings import *

DEBUG = False

ALLOWED_HOSTS = [
    'ec2-3-134-61-181.us-east-2.compute.amazonaws.com',
    '3.134.61.181'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': 'lubricentro_myc',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '3.134.61.181',   # Or an IP Address that your DB is hosted on
        'PORT': '5432',
    }
}

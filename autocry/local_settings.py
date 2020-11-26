from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # new
# DEFAULT_FROM_EMAIL = 'takvor@students.softuni.bg'
# EMAIL_HOST = 'smtp.sendgrid.net'  # new
# EMAIL_HOST_USER = 'apikey'  # new
# EMAIL_HOST_PASSWORD = 'your apikey goes here'  # new
# EMAIL_PORT = 587  # new
# EMAIL_USE_TLS = True  # new

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auto_cry',
        'USER': 'postgres',
        'PASSWORD': 'admin'
    }
}

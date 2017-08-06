import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

CELERY_ALWAYS_EAGER = True

if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(os.getcwd(), 'apimocker', 'static'),
    )

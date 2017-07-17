import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(os.getcwd(), 'apimocker', 'static'),
    )

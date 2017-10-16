import os

DEBUG = True

if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(os.getcwd(), 'apimocker', 'static'),
    )

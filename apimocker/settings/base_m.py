LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

RAVEN_CONFIG = {
    'dsn': RAVEN_CONFIG_DSN, # noqa
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

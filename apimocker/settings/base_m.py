LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

RAVEN_CONFIG = {
    'dsn': RAVEN_CONFIG_DSN,
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'
SHORT_URL_MAX_LEN = 6
HOSTNAME = 'http://api-mocker-django.herokuapp.com'
LOGFILE_INFO = os.path.join(os.path.dirname(BASE_DIR), "logs", "info.log")
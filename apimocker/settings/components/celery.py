BROKER_URL = REDIS_MOCKER_URL # noqa
CELERY_RESULT_BACKEND = REDIS_MOCKER_URL # noqa

# Timezone for celery
CELERY_TIMEZONE = 'Europe/Warsaw'

CELERY_CREATE_MISSING_QUEUES = True

# If Celery removes the existing logger, nothing will go to Sentry
CELERYD_HIJACK_ROOT_LOGGER = False

# If enabled stdout and stderr will be redirected to the current logger
CELERY_REDIRECT_STDOUTS = False

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 600

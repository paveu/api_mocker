LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['main', 'sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'main': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'celery': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
    },
}

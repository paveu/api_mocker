LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['main', 'sentry'],
    },
    'formatters': {
        # 'logstash': {
        #     '()': 'apimocker.utils.log.LogstashFormatter',
        # },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'main': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['main'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['main'],
            'level': 'ERROR',
            'propagate': False,
        },
        'raven': {
            'handlers': ['main'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

# if RACK:
#     LOGGING['handlers']['main'] = {
#         'level': 'INFO',
#         'class': 'logging.FileHandler',
#         'filename': '/var/log/app.log',
#         'formatter': 'logstash'
#     }

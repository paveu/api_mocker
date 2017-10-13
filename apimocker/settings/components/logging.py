from __future__ import absolute_import

import logging
from logstash.formatter import LogstashFormatterVersion1


class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            'RemovedInDjango110Warning',
            'RemovedInDjango20Warning',
        ]
        # Return false to suppress message.
        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])


class LogstashFormatter(LogstashFormatterVersion1):
    def _stringify(self, s):
        if isinstance(s, unicode):
            s = s.decode('utf-8', 'ignore')

        return str(s)

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'host': self.host,
            'pathname': record.pathname,
            'tags2': self.tags,
            'message': record.getMessage(),
            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
            'ex': {k: self._stringify(v) for k, v in self.get_extra_fields(record).iteritems()},
        }

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['main', 'sentry'],
    },
    'formatters': {
        'logstash': {
            '()': LogstashFormatter,
        },
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
        'apimocker.utils.middlewares': {
            'handlers': ['main'],
            'level': 'INFO',
            'propagate': False,
        },
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
    'filters': {
        'suppress_deprecated': {
            '()': SuppressDeprecated,
        }
    },
}

if ENVIRONMENT == 'production':  # noqa
    LOGGING['handlers']['main'] = {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': '/var/log/app.log',
        'formatter': 'logstash',
        'filters': ['suppress_deprecated'],
    }

import logging
logging.disable(logging.CRITICAL)


CELERY_ALWAYS_EAGER = True

INSTALLED_APPS += ( # noqa
    'django_nose',
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--nologcapture',
    '-s',
    '--tests=tests',
]

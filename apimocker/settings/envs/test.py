import logging
logging.disable(logging.CRITICAL)

CELERY_ALWAYS_EAGER = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

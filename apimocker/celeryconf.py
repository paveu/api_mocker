from __future__ import absolute_import, unicode_literals

import os
import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apimocker.settings')

app = celery.Celery(
    'apimocker',
    broker=settings.REDIS_MOCKER_URL,
    backend=settings.REDIS_MOCKER_URL,
    namespace='CELERY'
)
app.conf.update(
    task_always_eager=False,
    task_default_queue='celery',
    task_default_exchange='celery',
    task_default_routing_key='celery',
    accept_content=['application/json'],
    task_serializer='json',
    result_serializer='json',
    worker_hijack_root_logger=False,
    worker_disable_rate_limits=False,
    result_expires=600,
    timezone='Europe/Warsaw',
    worker_redirect_stdouts=False,
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

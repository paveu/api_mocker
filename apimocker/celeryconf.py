from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


app = Celery(
    'mocker',
    broker=settings.REDIS_MOCKER_URL,
)

app.conf.update(
    beat_schedule={
        'warehouse-synchro': {
            'task': 'mocker.tasks.cron_synchro',
            'schedule': crontab(hour='*', minute='*')
        },
    },
    worker_hijack_root_logger=False,
)


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

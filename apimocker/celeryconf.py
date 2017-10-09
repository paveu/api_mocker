from __future__ import absolute_import, unicode_literals

import os
import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apimocker.settings')

app = celery.Celery(
    'apimocker',
    broker=settings.REDIS_MOCKER_URL,
)
app.conf.update(
    worker_hijack_root_logger=False,
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from __future__ import absolute_import

from .celeryconf import app  # noqa
task = app.task  # noqa

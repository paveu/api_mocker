import logging

from django.http import Http404


logger = logging.getLogger(__name__)


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, (Http404,)):
            logger.exception('Exception handling request for ' + request.path)

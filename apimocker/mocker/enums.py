# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


class HTTP_METHODS(object):
    POST = 'POST'
    GET = 'GET'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'

    choices = (
        (POST, 'POST'),
        (GET, 'GET'),
        (PATCH, 'PATCH'),
        (PUT, 'PUT'),
        (HEAD, 'HEAD'),
        (OPTIONS, 'OPTIONS'),
    )


class CONTENT_TYPES(object):
    # TODO: check if all content types are included
    APP_JSON = 'application/json'
    APP_FORM_URLENCODED = 'application/x-www-form-urlencoded'
    APP_XML = 'application/xhtml+xml'
    DATA = 'multipart/form-data'
    TEXT_CSS = 'text/css'
    TEXT_CSV = 'text/csv'
    TEXT_HTML = 'text/html'
    TEXT_JSON = 'text/json'
    TEXT_PLAIN = 'text/plain'
    TEXT_XML = 'text/xml'

    choices = (
        (APP_JSON, _('application/json')),
        (APP_FORM_URLENCODED, _('application/x-www-form-urlencoded')),
        (APP_XML, _('application/xhtml+xml')),
        (DATA, _('multipart/form-data')),
        (TEXT_CSV, _('text/css')),
        (TEXT_CSS, _('text/csv')),
        (TEXT_HTML, _('text/html')),
        (TEXT_JSON, _('text/json')),
        (TEXT_PLAIN, _('text/plain')),
        (TEXT_XML, _('text/xml')),
    )
    alist = [ct[0] for ct in choices]


class STATUS_CODES(object):
    # TODO: add more codes
    OK = 200
    BAD_REQUEST = 400
    ANAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500

    choices = (
        (OK, 200),
        (BAD_REQUEST, 400),
        (ANAUTHORIZED, 401),
        (PAYMENT_REQUIRED, 402),
        (FORBIDDEN, 403),
        (INTERNAL_SERVER_ERROR, 500),
    )


SUCCESS_FORM_ACTION_MSG = _("Thanks for mocking an API !")
SHORT_URL_MAX_LEN = 6

# -*- coding: utf-8 -*-

import json
import logging
import random
import string
import urlparse
from requests import request

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect

from .enums import CONTENT_TYPES, HTTP_METHODS, SHORT_URL_MAX_LEN
from .models import Mocker, ResponseLog

logger = logging.getLogger(__name__)


def get_hashed_id():
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        hashed_id = ''.join(random.choice(char) for _ in range(SHORT_URL_MAX_LEN))
        try:
            Mocker.objects.get(hashed_id=hashed_id)
        except Mocker.DoesNotExist:
            return hashed_id


class Requester(object):
    def __init__(self, hashed_id, requested_http_method, requested_content_type, absolute_uri, forced_format):
        self.hashed_id = hashed_id
        self.requested_http_method = requested_http_method
        self.requested_content_type = requested_content_type
        self.absolute_uri = absolute_uri
        self.forced_format = forced_format

    def make_callback(self, mock, response):
        logger.info("mocker:make-callback", extra={
            'callback_address': mock.callback_address,
            'callback_content_type': mock.callback_content_type,
            'mocker_id': mock.id,
        })

        self.make_http_request(
            url=mock.callback_address,
            requested_http_method=HTTP_METHODS.POST,
            requested_content_type=mock.callback_content_type,
            mock=mock,
            callback_response=response,
        )

    def make_response(self, mock, response):
        logger.info("mocker:make-response", extra={'mocker_id': mock.id})

        if response:
            ResponseLog.objects.create(headers=response.headers, content=response.content,  mocker=mock)

            if mock.callback_address:
                self.make_callback(mock, response=response)

            is_content_type_json = mock.allowed_content_type == CONTENT_TYPES.APP_JSON
            return HttpResponse(
                content=json.dumps(response.content) if is_content_type_json else response.content,
                content_type=mock.response_setting.content_type if mock.response_setting else None,
                status=mock.response_setting.status_code if mock.response_setting else None,
            )
        logger.warning("mocker:no-response-object-found", extra={'mocker_id': mock.id})

    def process_request(self):
        try:
            mock = Mocker.objects.get(hashed_id=self.hashed_id)
            logger.info("mocker:validate-provided-mock-id", extra={'mocker_id': mock.id})
        except Mocker.DoesNotExist:
            return redirect("/")

        params = self.absolute_uri[self.absolute_uri.find(self.hashed_id)+len(self.hashed_id)+1:]
        url = urlparse.urljoin(mock.destination_address, params)
        if self.requested_http_method in mock.allowed_http_method \
                and self.requested_content_type == mock.allowed_content_type:

            if self.forced_format == "json":
                response = self.make_http_request(url, self.requested_http_method, CONTENT_TYPES.APP_JSON, mock)
                return self.make_response(mock, response)

            if self.requested_content_type == mock.allowed_content_type:
                response = self.make_http_request(url, self.requested_http_method, self.requested_content_type, mock)
                return self.make_response(mock, response)
        return HttpResponseForbidden()

    def make_http_request(self, url, requested_http_method, requested_content_type, mock, callback_response=None):
        logger.info("mocker:make-http-request", extra={
            'url': url,
            'requested_http_method': requested_http_method,
            'requested_content_type': requested_content_type,
            'mocker_id': mock.id,
        })
        ret_data = None
        ret_json = None
        if callback_response:
            if callback_response.status_code != 200:
                ret_data = callback_response.reason
            else:
                ret_data = callback_response.text
                try:
                    ret_json = callback_response.json
                except AttributeError:
                    pass
        kw = {
            'data': ret_data,
            'json': ret_json,
            'params': None,
            'headers': {'Content-type': requested_content_type},
            'allow_redirects': False,
        }

        custom_headers = mock.customheader_set.order_by('id').values_list('key', 'value')
        for key, value in custom_headers:
            if key == 'Content-type':
                continue
            kw['headers'][key] = value

        if kw in [HTTP_METHODS.POST, HTTP_METHODS.PUT, HTTP_METHODS.DELETE]:
            kw['allow_redirects'] = True
        return request(requested_http_method, url, **kw)

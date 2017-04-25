# -*- coding: utf-8 -*-

import json
import logging
import random
import string
import urlparse

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect

from .enums import CONTENT_TYPES, HTTP_METHODS, SHORT_URL_MAX_LEN
from .models import Mocker, APILog
from .tasks import make_http_request

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
        self.requested_content_type = requested_content_type
        self.absolute_uri = absolute_uri
        self.forced_format = forced_format

    def make_callback(self, mock, response):
        # TODO: make it async
        make_http_request(
            url=mock.callback_address,
            requested_http_method=HTTP_METHODS.POST,
            requested_content_type=mock.callback_content_type,
            data=response,
        )

    def make_response(self, mock, response):
        if response:
            if mock.callback_address:
                self.make_callback(mock, response=response)

            response_data = mock.response_data
            if response_data:
                api_log = APILog.objects.create(
                    address=mock.destination_address,
                    response=response.content,
                )
                mock.api_log = api_log
                mock.save()

                is_content_type_json = mock.allowed_content_type == CONTENT_TYPES.APP_JSON
                # TODO: make content=json.dump(response) ?
                return HttpResponse(
                    content=json.dumps(response.content) if is_content_type_json else response.content,
                    content_type=response_data.content_type,
                    status=response_data.status_code,
                )

    def process_request(self):
        try:
            mock = Mocker.objects.get(hashed_id=self.hashed_id)
        except Mocker.DoesNotExist:
            return redirect("/")

        params = self.absolute_uri[self.absolute_uri.find(self.hashed_id)+len(self.hashed_id)+1:]
        url = urlparse.urljoin(mock.destination_address, params)

        if self.requested_http_method == mock.allowed_http_method \
                and self.requested_content_type == mock.allowed_content_type:

            if self.forced_format == "json":
                response = make_http_request(url, self.requested_http_method, CONTENT_TYPES.APP_JSON)
                return self.make_response(mock, response)
            # TODO: for and if could be removed class and foo
            for ct in CONTENT_TYPES.alist:
                if ct == self.requested_content_type:
                    response = make_http_request(url, self.requested_http_method, self.requested_content_type)
                    return self.make_response(mock, response)
        return HttpResponseForbidden()

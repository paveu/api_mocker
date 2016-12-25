import json
import logging
import requests
import random
import string
from django.conf import settings
from django.http import JsonResponse
from .models import Mocker

logger = logging.getLogger(__name__)


def get_hashed_id():
    """
    This will generate unique hashed ID for mocking API
    """
    length = settings.SHORT_URL_MAX_LEN
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        hashed_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Mocker.objects.get(hashed_id=hashed_id)
        except Mocker.DoesNotExist:
            return hashed_id


def make_http_request(url, requested_http_method, requested_content_type, data=None):
    """
    TBD
    :param url:
    :param requested_http_method:
    :param requested_content_type:
    :param data:
    :return:
    """
    resp = None

    if data:
        if data.status_code != 200:
            data = data.reason
        else:
            data = data.text

    if requested_content_type == 'application/json':
        if data:
            data = json.dumps(data)

    destination_header = {'Content-type': requested_content_type}

    if requested_http_method == "GET":
        resp = requests.get(url, data=data, headers=destination_header)
    elif requested_http_method == "POST":
        resp = requests.post(url, data=data, headers=destination_header)
    elif requested_http_method == "PATCH":
        resp = requests.patch(url, data=data, headers=destination_header)
    elif requested_http_method == "PUT":
        resp = requests.put(url, data=data, headers=destination_header)
    return resp


def make_callback(hashed_id, resp):
    """
    Make callback API
    """

    mock = Mocker.objects.get(hashed_id=hashed_id)
    callback_address = mock.callback_address
    callback_content_type = mock.callback_content_type
    make_http_request(url=callback_address,
                      requested_http_method="POST",
                      requested_content_type=callback_content_type,
                      data=resp)


def process_request(hashed_id,
                    requested_http_method,
                    requested_content_type,
                    absolute_uri,
                    forced_format):
    """
    Performing HTTP operations on mocked API
    """

    mock = Mocker.objects.get(hashed_id=hashed_id)
    original_destination_address = mock.original_destination_address
    callback_address = mock.callback_address
    mocked_allowed_http_method = mock.mocked_allowed_http_method
    mocked_allowed_content_type = mock.mocked_allowed_content_type

    params = absolute_uri[absolute_uri.find(hashed_id)+len(hashed_id)+1:]
    url = ''.join([original_destination_address, params])

    # Check if requested http method is allowed
    if requested_http_method == mocked_allowed_http_method:
        # Check if requested content_type is allowed
        if requested_content_type == mocked_allowed_content_type:

            if requested_content_type == 'application/json' or forced_format == "json":
                resp = make_http_request(url, requested_http_method, requested_content_type)
                if resp:
                    if callback_address:
                        make_callback(hashed_id, resp=resp)
                    return JsonResponse(json.dumps(resp.text), safe=False, status=resp.status_code)
                return JsonResponse({"status": "HTTP Requests internal error. No Requests object. X-files"}, status=500)
            elif requested_content_type == 'text/xml':
                pass
        else:
            return JsonResponse({"status": "Requested Content type is not allowed"}, status=405)
    else:
        return JsonResponse({"status": "Requested HTTP method is not allowed"}, status=405)

import sys
import json
import logging
import requests
import random
import string
import urlparse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import Mocker
reload(sys)
sys.setdefaultencoding('utf8')
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
    To be explained...
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
    Make callback to predefined address
    """

    mock = Mocker.objects.get(hashed_id=hashed_id)
    callback_address = mock.callback_address
    callback_content_type = mock.callback_content_type

    make_http_request(url=callback_address,
                      requested_http_method="POST",
                      requested_content_type=callback_content_type,
                      data=resp)


def process_request(hashed_id, requested_http_method, requested_content_type, absolute_uri, forced_format):
    """
    Performing HTTP operations on mocked API
    """
    # print("hashed_id", hashed_id)
    mock = Mocker.objects.get(hashed_id=hashed_id)
    # print("mock", mock)
    original_destination_address = mock.original_destination_address
    # print("original_destination_address", original_destination_address)
    callback_address = mock.callback_address
    # print("callback_address", callback_address)
    mocked_allowed_http_method = mock.mocked_allowed_http_method
    # print("mocked_allowed_http_method", mocked_allowed_http_method)
    mocked_allowed_content_type = mock.mocked_allowed_content_type
    # print("mocked_allowed_content_type", mocked_allowed_content_type)
    # print("absolute_uri", absolute_uri)
    params = absolute_uri[absolute_uri.find(hashed_id)+len(hashed_id)+1:]
    url = urlparse.urljoin(original_destination_address, params)
    # print("url", url)

    # Check if requested http method is allowed
    if requested_http_method == mocked_allowed_http_method:
        # Check if requested content_type is allowed
        if requested_content_type == mocked_allowed_content_type:

            if requested_content_type == 'application/json' or forced_format == "json":
                resp = make_http_request(url, requested_http_method, requested_content_type)
                print("url2", url)
                print("requested_http_method", requested_http_method)
                print("requested_content_type", requested_content_type)
                print("resp", resp)
                if resp:
                    if callback_address:
                        make_callback(hashed_id, resp=resp)
                    return JsonResponse(json.dumps(resp.text), safe=False, status=resp.status_code)
                return JsonResponse({"status": "HTTP Requests internal error"}, status=500)

            elif requested_content_type == 'text/plain':
                resp = make_http_request(url, requested_http_method, requested_content_type)
                if resp:
                    if callback_address:
                        make_callback(hashed_id, resp=resp)
                    return HttpResponse(content=resp.text, content_type='text/plain', status=resp.status_code)
                return HttpResponse(content="HTTP Requests internal error", content_type='text/plain', status=500)

        else:
            return JsonResponse({"status": "Requested Content type is not allowed"}, status=405)
    else:
        return JsonResponse({"status": "Requested HTTP method is not allowed"}, status=405)

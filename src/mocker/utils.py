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
        except:
            return hashed_id


def make_callback(hashed_id, data):
    """
    Make callback API
    """

    mock = Mocker.objects.get(hashed_id=hashed_id)
    callback_api = mock.callback_address
    callback_content_type = mock.callback_content_type

    try:
        data = json.dumps(data.json())
    except ValueError:
        data = {'status': 'No JSON object could be decoded'}

    if callback_content_type == 'application/json':
        callback_header = {'Content-type': str(callback_content_type)}
        callback = requests.post(callback_api, data=data, headers=callback_header)
        return callback.status_code


def process_request(hashed_id,
                    requested_allowed_http_method,
                    requested_content_type,
                    absolute_uri,
                    forced_format):
    """
    Perfornming HTTP operations on mocked API
    """
    mock = Mocker.objects.get(hashed_id=hashed_id)
    
    original_destination_address = mock.original_destination_address
    callback_api = mock.callback_address

    allowed_allowed_http_method = mock.allowed_http_method
    allowed_content_type = mock.allowed_destination_content_type

    url = absolute_uri
    params = url[url.find(hashed_id)+len(hashed_id)+1:]

    # check if http method is allowed
    if requested_allowed_http_method == allowed_allowed_http_method:
        # check if content_type is allowed
        if requested_content_type == str(allowed_content_type):
            url = ''.join([original_destination_address, params])

            if requested_content_type == 'application/json' or forced_format == "json":
                destination_header = {'Content-type': str(requested_content_type)}
                if requested_allowed_http_method == "GET":
                    r = requests.get(url, headers=destination_header)
                elif requested_allowed_http_method == "POST":
                    r = requests.post(url, headers=destination_header)
                elif requested_allowed_http_method == "PATCH":
                    r = requests.patch(url, headers=destination_header)            
                elif requested_allowed_http_method == "PUT":
                    r = requests.put(url, headers=destination_header)  
                else:
                    return JsonResponse({"status": "Something went wrong"}, status=500)
                    
                if r.status_code == requests.codes.ok:
                    if callback_api:
                        response = make_callback(hashed_id, data=r)
                        #TODO: add handler for status codes
                        print("callback status_code", response)
                    logging.info("Destination API: %s, response: %s" % (url, r.text))
                    try:
                        data = r.json()
                        status_code = r.status_code
                    except ValueError:
                        data = {'status': 'No JSON object could be decoded'}
                        status_code = 500
                    return JsonResponse(json.dumps(data), safe=False, status=status_code)
                else:
                    return JsonResponse({"status": "Something went wrong"}, status=r.status_code)
        else:
            return JsonResponse({"status": "Content type: text/plain is not allowed"}, status=405)
    else:
        return JsonResponse({"status": "Requested HTTP method is not allowed"}, status=405)



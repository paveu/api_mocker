import requests
import json
import logging
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render

from .models import Mocker

logging.basicConfig(filename=settings.LOGFILE_INFO, level=logging.INFO)
logger = logging.getLogger(__name__)

def make_callback(short_id, data):
    """
    Make callback API
    """

    mock = Mocker.objects.get(short_id=short_id)
    callback_api = mock.return_address
    return_content_type = mock.return_content_type
    try:
        data = json.dumps(data.json())
    except ValueError:
        data = {'status': 'No JSON object could be decoded'}
    if return_content_type == 'application/json':
        callback_header = {'Content-type': str(return_content_type)}
        callback = requests.post(callback_api, data=data, headers=callback_header)
        return callback.status_code

def process_request(short_id,
                    requested_http_method,
                    requested_content_type,
                    absolute_uri,
                    forced_format):
    """
    Perfornming HTTP operations on mocked API
    """
    mock = Mocker.objects.get(short_id=short_id)
    
    destination_address = mock.destination_address
    callback_api = mock.return_address

    allowed_http_method = mock.http_method
    allowed_content_type = mock.destination_content_type

    url = absolute_uri
    params = url[url.find(short_id)+len(short_id)+1:]

    # check if http method is allowed
    if requested_http_method == allowed_http_method:
        # check if content_type is allowed
        if requested_content_type == str(allowed_content_type):
            url = ''.join([destination_address, params])

            if requested_content_type == 'application/json' or forced_format == "json":
                destination_header = {'Content-type': str(requested_content_type)}
                if requested_http_method == "GET":
                    r = requests.get(url, headers=destination_header)
                elif requested_http_method == "POST":
                    r = requests.post(url, headers=destination_header)
                elif requested_http_method == "PATCH":
                    r = requests.patch(url, headers=destination_header)            
                elif requested_http_method == "PUT":
                    r = requests.put(url, headers=destination_header)  
                else:
                    return JsonResponse({"status": "Something went wrong"}, status=500)
                    
                if r.status_code == requests.codes.ok:
                    if callback_api:
                        response = make_callback(short_id, data=r)
                        #TODO: add handler for status codes
                        print("callback status_code", response)
                    logging.info("Destination API: %s, response: %s" % (url, str(r.content)))
                    return JsonResponse(json.dumps(r.json()), safe=False, status=r.status_code)
                else:
                    return JsonResponse({"status": "Something went wrong"}, status=r.status_code)
        else:
            return JsonResponse({"status": "Content type: text/plain is not allowed"}, status=405)
    else:
        return JsonResponse({"status": "Requested HTTP method is not allowed"}, status=405)



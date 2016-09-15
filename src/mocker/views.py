import random
import requests
import string
import json
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import MockerForm
from .models import Mocker
from .utils import make_callback

logging.basicConfig(filename=settings.LOGFILE_INFO, level=logging.INFO)
logger = logging.getLogger(__name__)

def home(request):
    """
    home view
    """
    return render(request, "home.html", {'form': MockerForm()})


def job_post_view(request):
    """
    It performs form validation along with creating mocked address.
    """

    form = MockerForm(request.POST)
    if form.is_valid():
        # get unique hashed address for original destination address
        short_id = get_short_id()
        mocked_url = ''.join([settings.HOSTNAME, "/", short_id, "/"])
        
        form_mock = form.save(commit=False)
        form_mock.short_id = short_id
        form_mock.mocked_address = mocked_url
        form_mock.save()
        
        context = {
                  "destination_url": form_mock.destination_address,
                  "mocked_url": mocked_url,
                  "action_msg": "Thanks for mocki API!"
                  }
        messages.success(request, "Operation completed")
        return render(request, "action_status.html", context)
    else:
        messages.warning(request, "Something went wrong. Form is not valid")
        return render(request, "action_status.html", {"action_msg": None})


def get_short_id():
    """
    This will generate unique mshort ID for mocking API
    """
    length = settings.SHORT_URL_MAX_LEN
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Mocker.objects.get(short_id=short_id)
        except:
            return short_id


@csrf_exempt
def mocked_api_view(request, short_id):
    """
    Perfornming HTTP operations on mocked API
    """
    mock = Mocker.objects.get(short_id=short_id)
    
    destination_address = mock.destination_address
    callback_api = mock.return_address

    allowed_http_method = mock.http_method
    allowed_content_type = mock.destination_content_type

    url = request.build_absolute_uri()
    params = url[url.find(short_id)+len(short_id)+1:]
    requested_content_type = request.content_type
    # check if http method is allowed
    forced_format = request.GET.get('format','')

    if request.method == allowed_http_method:
        # check if content_type is allowed
        if requested_content_type == str(allowed_content_type):
            url = ''.join([destination_address, params])

            if request.method == "GET":
                if requested_content_type == 'application/json' or forced_format == "json":
                    destination_header = {'Content-type': str(requested_content_type)}
                    r = requests.get(url, headers=destination_header)
                    if r.status_code == requests.codes.ok:
                        if callback_api:
                            response = make_callback(short_id, data=r)
                            #TODO: add handler for status codes
                            print("callback status_code", response)
                        logging.info("Destination API: %s, response: %s" % (url, r.content))
                        return JsonResponse(json.dumps(r.json()), safe=False, status=r.status_code)
                    else:
                        return JsonResponse({"status": "Error"}, status=r.status_code)
            elif request.method == "POST":
                if requested_content_type == 'application/json' or forced_format == "json":
                    destination_header = {'Content-type': str(requested_content_type)}
                    r = requests.post(url, headers=destination_header)
                    if r.status_code == requests.codes.ok:
                        if callback_api:
                            response = make_callback(short_id, data=r)
                            #TODO: add handler for status codes
                            print("callback status_code", response)
                        logging.info("Destination API: %s, response: %s" % (url, r.content))
                        return JsonResponse(json.dumps(r.json()), safe=False, status=r.status_code)
                    else:
                        return JsonResponse({"status": "Error"}, status=r.status_code)
        else:
            if str(requested_content_type) == 'text/plain':
                messages.warning(request, "Content type: text/plain is not allowed")
                return render(request, "error.html",{})
        return JsonResponse({"status": "Requested content type is not allowed"}, status=403)
    else:
        return JsonResponse({"status": "Requested HTTP method is not allowed"}, status=405)

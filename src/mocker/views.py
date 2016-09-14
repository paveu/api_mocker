import random
import requests
import string
import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from mocker.forms import MockerForm
from mocker.models import Mocker
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

def home(request):
    """
    home view
    """
    return render(request, "home.html", {'form': MockerForm()})

def job_post_view(request):
    """
    job post view
    """

    form = MockerForm(request.POST)
    if form.is_valid():
        short_id = get_short_id()
        
        form_mock = form.save(commit=False)
        form_mock.short_id = short_id
        form_mock.save()
        
        mocked_url = ''.join([settings.HOSTNAME, "/", form_mock.short_id, "/"])
        context = {
                  "destination_url": form_mock.destination_address,
                  "mocked_url": mocked_url,
                  "action_msg": "Thanks for submitting the job!"
                  }
       
        messages.success(request, "Operation completed")
        return render(request,
                      "action_status.html",
                      context)
    else:
        messages.warning(request, "Something went wrong. Form is not valid")
        return render(request,
                      "action_status.html",
                      {"action_msg": None})


def get_short_id():
    """
    This will generate the unique mock address for particular url
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
    """
    mock_obj = Mocker.objects.get(short_id=short_id)
    
    destination_address = mock_obj.destination_address
    allowed_http_method = mock_obj.http_method
    allowed_content_type = mock_obj.destination_content_type
    
    url = request.build_absolute_uri()
    params = url[url.find(short_id)+len(short_id)+1:]
    requested_content_type = request.content_type
    #print("params", params)
    #print("requested_content_type", requested_content_type)
    #print("request.method", request.method)
    #print("request.method", request.method)
    #print("allowed_http_method", allowed_http_method)
    if request.method != allowed_http_method:
        #TODO: raise error
        print("Requested HTTP method is not allowed")
    else:
        url = ''.join([destination_address, params])
        headers = {'Content-type': str(requested_content_type)}
        if requested_content_type != str(allowed_content_type):
            if str(requested_content_type) == 'text/plain':
                messages.warning(request, "Content type: text/plain is not allowed")
                return render(request, "api_lookup.html",{})
            #TODO: raise error
            print("Requested content type is not allowed")
        else:
            if request.method == "GET":
                r = requests.get(url, headers=headers)
                if r.status_code == requests.codes.ok:
                    return JsonResponse(json.dumps(r.json()), safe=False, status=200)
                else:
                    return JsonResponse({}, status=406)
            elif request.method == "POST":
                r = requests.post(url, headers=headers)
                if r.status_code == requests.codes.ok:
                    return JsonResponse(json.dumps(r.json()), safe=False, status=200)
                else:
                    return JsonResponse({}, status=406)
import random
import string
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import MockerForm
from .models import Mocker
from .utils import process_request


def home(request):
    """
    It prints out Mock API form
    """
    return render(request, "home.html", {'form': MockerForm()})


def job_post_view(request):
    """
    It performs form validation along with creating mocked address.
    """

    form = MockerForm(request.POST)
    if form.is_valid():
        # get unique hashed address for original destination address
        short_id = get_hashed_id()
        mocked_url = ''.join([settings.HOSTNAME, "/", short_id, "/"])
        
        form_mock = form.save(commit=False)
        form_mock.short_id = short_id
        form_mock.mocked_address = mocked_url
        form_mock.save()
        
        context = {
                  "destination_url": form_mock.destination_address,
                  "mocked_url": mocked_url,
                  "action_msg": "Thanks for mocking an API !"
                  }
        messages.success(request, "Operation completed with succcess")
        return render(request, "action_status.html", context)
    else:
        messages.warning(request, "Something went wrong. Form is not valid")
        return render(request, "action_status.html", {"action_msg": None})


def get_hashed_id():
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
    Perfornming HTTP based on incoming request. It uses short_id to recognize
    mocked API address
    """

    return process_request(short_id=short_id,
        requested_http_method=request.method,
        requested_content_type=request.content_type,
        absolute_uri=request.build_absolute_uri(),
        forced_format= request.GET.get('format','')
        )

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView

from .forms import MockerForm
from .utils import process_request, get_hashed_id
from .models import Mocker


class CreateMockerView(CreateView):
    template_name = "create_mocker.html"
    form_class = MockerForm
    model = Mocker
#
# class MyFormView(View):
#     form_class = MyForm
#     initial = {'key': 'value'}
#     template_name = 'form_template.html'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')
#
#         return render(request, self.template_name, {'form': form})


def job_post_view(request):
    """
    It performs form validation along with creating mocked address.
    """

    form = MockerForm(request.POST)
    if form.is_valid():
        # Get unique hashed for IP to be mocked
        hashed_id = get_hashed_id()
        mocked_url = ''.join([settings.HOSTNAME, "/", hashed_id, "/"])

        form_mock = form.save(commit=False)
        form_mock.hashed_id = hashed_id
        form_mock.mocked_address = mocked_url
        form_mock.save()

        context = {
            "destination_url": form_mock.original_destination_address,
            "mocked_url": mocked_url,
            "action_msg": "Thanks for mocking an API !"
        }

        messages.success(request, "Operation completed with success")
        return render(request, "action_status.html", context)
    else:
        messages.warning(request, "Something went wrong. Form is not valid")
        return render(request, "action_status.html", {"action_msg": None})


@csrf_exempt
def mocked_api_view(request, hashed_id):
    """
    Processing mocked API based on incoming request. It uses hashed_id to recognize
    mocked API address
    """

    return process_request(
        hashed_id=hashed_id,
        requested_http_method=request.method,
        requested_content_type=request.content_type,
        absolute_uri=request.build_absolute_uri(),
        forced_format=request.GET.get('format', ''),
    )

# class PublisherBookList(ListView):
#
#     template_name = 'books/books_by_publisher.html'
#
#     def get_queryset(self):
#         self.publisher = get_object_or_404(Publisher, name=self.args[0])
#         return Book.objects.filter(publisher=self.publisher)
# -*- coding: utf-8 -*-
import logging

from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView

from .enums import SUCCESS_FORM_ACTION_MSG
from .forms import MockerForm
from .utils import Requester, get_hashed_id
from .models import Mocker

logger = logging.getLogger(__name__)


class CreateMockerView(CreateView):
    template_name = "create_mocker.html"
    form_class = MockerForm
    model = Mocker


class ProcessMockFormView(FormView):
    form_class = MockerForm
    template_name = "action_status.html"

    def form_valid(self, form):
        hashed_id = get_hashed_id()
        mocked_url = ''.join([self.request.build_absolute_uri('/'), hashed_id, "/"])

        form = form.save(commit=False)
        form.hashed_id = hashed_id
        form.mocked_address = mocked_url
        form.save()
        context = {
            "destination_url": form.destination_address,
            "mocked_url": mocked_url,
            "action_msg": SUCCESS_FORM_ACTION_MSG,
        }
        messages.success(self.request, "Operation completed with success")
        return self.render_to_response(context)

    def form_invalid(self, form):
        messages.warning(self.request, "Something went wrong. Form is not valid")
        return self.render_to_response(context={})


class ResolveMockedAddressView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ResolveMockedAddressView, self).dispatch(request, *args, **kwargs)

    def _process(self, request, hashed_id):
        return Requester(
            hashed_id=hashed_id,
            requested_http_method=request.method,
            requested_content_type=request.content_type,
            absolute_uri=request.build_absolute_uri(),
            forced_format=request.GET.get('format', ''),
        ).process_request()

    def post(self, request, hashed_id):
        return self._process(request, hashed_id)

    def get(self, request, hashed_id):
        return self._process(request, hashed_id)

    def patch(self, request, hashed_id):
        return self._process(request, hashed_id)

    def put(self, request, hashed_id):
        return self._process(request, hashed_id)

    def delete(self, request, hashed_id):
        return self._process(request, hashed_id)

    def head(self, request, hashed_id):
        return self._process(request, hashed_id)

    def options(self, request, hashed_id):
        return self._process(request, hashed_id)

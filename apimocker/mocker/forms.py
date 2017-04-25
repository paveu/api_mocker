# -*- coding: utf-8 -*-

import logging

from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions

from .models import Mocker

logger = logging.getLogger(__name__)


class MockerForm(forms.ModelForm):
    class Meta:
        model = Mocker
        fields = [
            'destination_address',
            'allowed_http_method',
            'allowed_content_type',
            'callback_address',
            'callback_content_type',
            'response_data',
        ]

    def __init__(self, *args, **kwargs):
        super(MockerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('process_mock_form_view')

        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                        href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
                )
        )

# -*- coding: utf-8 -*-
import logging

from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.bootstrap import FormActions, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, HTML, Layout, Submit

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
        ]

    def __init__(self, *args, **kwargs):
        super(MockerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('process_mock_form_view')
        self.helper.layout = Layout(
            Field('destination_address', autocomplete='off'),
            Field('allowed_content_type', autocomplete='off'),
            InlineCheckboxes('allowed_http_method'),
            Field('callback_address', autocomplete='off'),
            Field('callback_content_type', autocomplete='off'),
            FormActions(
                HTML("""<a role="button" class="btn btn-default" href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
            )
        )

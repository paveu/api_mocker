from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from .models import Mocker


class MockerForm(forms.ModelForm):
    class Meta:
        model = Mocker
        fields = ['destination_address',
            'http_method',
            'destination_content_type',
            'return_address',
            'return_content_type',
            ]

    def __init__(self, *args, **kwargs):
        super(MockerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = '/job-submit/'

        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                        href="{% url "home" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
                ))
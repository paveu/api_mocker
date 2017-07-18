import responses
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory

from apimocker.mocker.enums import CONTENT_TYPES, SUCCESS_FORM_ACTION_MSG, HTTP_METHODS
from apimocker.mocker.models import Mocker, ResponseContent
from tests.utils.factories import MockerFactory, ResponseSettingFactory


class CreatingMocker(TestCase):
    def setUp(self):
        Site.objects.create()
        ResponseSettingFactory()
        self.client = Client()
        self.factory = RequestFactory()

    def test_process_form_view(self):
        data = {
            'destination_address': 'http://jsonplaceholder.typicode.com/posts',
            'allowed_http_method': 'POST',
            'allowed_content_type': 'application/x-www-form-urlencoded',
            'callback_address': 'https://flask-app-pawelste.c9users.io/callback/',
            'callback_content_type': 'multipart/form-data',
            'response_data': 1,
        }
        response = self.client.post(reverse('process_mock_form_view'), data)
        self.assertTemplateUsed(response, 'action_status.html')
        self.assertEqual(response.context['action_msg'], SUCCESS_FORM_ACTION_MSG)
        self.assertIsNotNone(Mocker.objects.last().hashed_id)
        self.assertEqual(Mocker.objects.count(), 1)


class MockedAPI(TestCase):
    def setUp(self):
        Site.objects.create()
        self.client = Client()

    @responses.activate
    def test_mocked_api_with_post_method_and_json_contenttype_with_json_callback(self):
        self.mocker = MockerFactory(
            allowed_http_method=HTTP_METHODS.POST,
            allowed_content_type=CONTENT_TYPES.APP_JSON,
            callback_content_type=CONTENT_TYPES.APP_JSON,
        )
        responses.add(
            responses.POST,
            self.mocker.destination_address,
            body='{"Key": "val"}',
            status=200,
            content_type=CONTENT_TYPES.APP_JSON,
        )

        response = self.client.post(
            path=reverse('mocked_api_view', args=[self.mocker.hashed_id, '']),
            content_type=CONTENT_TYPES.APP_JSON,
        )
        self.assertEqual(response.status_code, 200)

        # Mocked API
        self.assertEqual(responses.calls[0].response.status_code, 200)

        # PUSH callback request to not mocked URL
        self.assertEqual(
            responses.calls[1].response.message,
            'Connection refused: {0}'.format(self.mocker.callback_address),
        )
        self.assertEqual(len(responses.calls), 2)

        # Response content saved to database
        self.assertEqual(ResponseContent.objects.count(), 1)

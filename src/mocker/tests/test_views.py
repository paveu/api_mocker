import mock
# import requests_mock
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from mocker.models import Mocker
from mocker.utils import get_hashed_id

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    pass


class TestBasic(TestCase):
    def setUp(self):
        self.client = Client()
        self.hashed_id = get_hashed_id()
        # self.mock_obj = MockFactory()
        self.mock_obj = Mocker.objects.create(
            creation_date=None,
            updation_date = None,
            original_destination_address = "http://jsonplaceholder.typicode.com",
            callback_address = "https://flask-app-pawelste.c9users.io/callback/",
            callback_content_type = "application/json",
            mocked_allowed_http_method = "POST",
            mocked_allowed_content_type = "application/json",
            mocked_address = "http://localhost:8000/RGNhou/",
            hashed_id = self.hashed_id,
        )

    def test_home_view(self):
        home_url = reverse("home")
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)

    def test_job_post_view(self):
        job_submit_url = reverse("job_submit_view")
        response = self.client.post(path=job_submit_url, data={'original_destination_address': 'http://jsonplaceholder.typicode.com',
                                                     'mocked_allowed_http_method': 'POST',
                                                     'mocked_allowed_content_type': 'application/json',
                                                     'callback_address': 'https://flask-app-pawelste.c9users.io/callback/',
                                                     'callback_content_type': 'application/json'
                                               }
                               )

        self.assertTemplateUsed(response, 'action_status.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['action_msg'], "Thanks for mocking an API !")

    # @mock.patch('requests.post', mock.Mock(side_effect=mocked_requests_get))
    @mock.patch('requests.post', mock.Mock(reason="dupa"))
    def test_job_post_view(self, mock_resp):
        mocked_api_url = reverse(viewname='mocked_api_view', args=[self.hashed_id, ''])
        response = self.client.post(path=mocked_api_url, data={}, content_type="application/json")
        print(response)
        print(mock_resp)
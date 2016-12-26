from django.core.urlresolvers import reverse
from django.test import TestCase, Client
# from mocker.factories import MockFactory
from mocker.models import Mocker
from mocker.utils import get_hashed_id


class TestBasic(TestCase):
    def setUp(self):
        self.client = Client()
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
            hashed_id = get_hashed_id(),
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


    def test_job_post_view(self):
        hashed_id = self.mock_obj.hashed_id
        hashed_id = ''.join([hashed_id, '/'])
        mocked_api_url = reverse('mocked_api_view', kwargs={'hashed_id': hashed_id})
        print("mocked_api_url", mocked_api_url)

        response = self.client.post(path=mocked_api_url, data={}, content_type="application/json")
        print(response)
        # print("response.context", response.context)
        # # print("mocked_api_url", mocked_api_url)
        # #
        # # process_request(hashed_id=hashed_id,
        # #                 requested_http_method=request.method,
        # #                 requested_content_type=request.content_type,
        # #                 absolute_uri=request.build_absolute_uri(),
        # #                 forced_format=request.GET.get('format', '')
        # #                 )
        # #
        # # pass

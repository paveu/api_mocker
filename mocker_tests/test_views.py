import mock
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from mocker.models import Mocker
from mocker.utils import get_hashed_id

from .utils import mocked_requests_post


class TestBasic(TestCase):
    def setUp(self):
        self.client = Client()
        self.hashed_id = get_hashed_id()
        self.mock_obj = Mocker.objects.create(
            creation_date=None,
            updation_date=None,
            original_destination_address="http://jsonplaceholder.typicode.com",
            callback_address="https://flask-app-pawelste.c9users.io/callback/",
            callback_content_type="application/json",
            mocked_allowed_http_method="POST",
            mocked_allowed_content_type="application/json",
            mocked_address="http://localhost:8000/RGNhou/",
            hashed_id=self.hashed_id,
        )

    def test_home_view(self):
        home_url = reverse("home")
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)

    def test_job_post_view(self):
        job_submit_url = reverse("job_submit_view")
        response = self.client.post(path=job_submit_url,
                                    data={'original_destination_address': 'http://jsonplaceholder.typicode.com',
                                          'mocked_allowed_http_method': 'POST',
                                          'mocked_allowed_content_type': 'application/json',
                                          'callback_address': 'https://flask-app-pawelste.c9users.io/callback/',
                                          'callback_content_type': 'application/json'}
                                    )

        self.assertTemplateUsed(response, 'action_status.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['action_msg'], "Thanks for mocking an API !")

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_job_post_view(self, mock_post):
        api_view = reverse(viewname='mocked_api_view', args=[self.hashed_id, ''])
        resp = self.client.post(path=api_view, data={}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)

        # print("resp_after_mock", resp) # JsonResponse status_code=200, "application/json">)
        # print("mock_post", mock_post) # <MagicMock name='post' id='4393451408'>
        # print("mock.call_args_list", mock_post.call_args_list)
        # ('mock.call_args_list', [call(u'http://jsonplaceholder.typicode.com', data=None, headers={'Content-type': 'application/json'}),
        #    call(u'https://flask-app-pawelste.c9users.io/callback/', data='"good"', headers={'Content-type': u'application/json'})])

        # mocked api call
        self.assertIn(mock.call(u'http://jsonplaceholder.typicode.com', data=None, headers={'Content-type': 'application/json'}), mock_post.call_args_list)
        # callback call
        self.assertIn(mock.call(u'https://flask-app-pawelste.c9users.io/callback/', data='"good_text"', headers={'Content-type': u'application/json'}), mock_post.call_args_list)

        self.assertEqual(len(mock_post.call_args_list), 2)
        self.assertTrue(mock_post.called)

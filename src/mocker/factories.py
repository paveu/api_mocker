from __future__ import unicode_literals
import factory
from mocker.models import Mocker


class MockFactory(factory.Factory):
    class Meta:
        model = Mocker

    creation_date = None
    updation_date = None
    original_destination_address = "http://jsonplaceholder.typicode.com"
    callback_address = "https://flask-app-pawelste.c9users.io/callback/"
    callback_content_type = "application/json"
    mocked_allowed_http_method = "POST"
    mocked_allowed_content_type = "application/json"
    mocked_address = "http://localhost:8000/RGNhou/"
    hashed_id = "RGNhou"

import factory
from mocker.models import Mocker


class MockFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Mocker

    original_destination_address = "http://jsonplaceholder.typicode.com"
    callback_address = "https://flask-app-pawelste.c9users.io/callback/"
    callback_content_type = "application/json"
    mocked_allowed_http_method = "GET"
    mocked_allowed_content_type = "application/json"
    mocked_address = "http://localhost:8000/RGNhou/"

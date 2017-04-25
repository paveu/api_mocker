import factory

from apimocker.mocker.enums import CONTENT_TYPES, STATUS_CODES, HTTP_METHODS
from apimocker.mocker.models import Mocker, ResponseSetting


class ResponseSettingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ResponseSetting

    content_type = CONTENT_TYPES.APP_JSON
    status_code = STATUS_CODES.OK


class MockerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Mocker

    destination_address = 'http://jsonplaceholder.typicode.com/posts'
    callback_address = 'https://flask-app-pawelste.c9users.io/callback/'
    callback_content_type = CONTENT_TYPES.APP_JSON
    allowed_http_method = HTTP_METHODS.POST
    allowed_content_type = CONTENT_TYPES.APP_JSON
    mocked_address = 'http://localhost:8000/RGNhou/'
    hashed_id = 'RGNhou'

    response_data = factory.SubFactory(ResponseSettingFactory)

import requests
import json
from .models import Mocker

def make_callback(short_id, data):
    """
    Make callback API
    """

    mock = Mocker.objects.get(short_id=short_id)
    callback_api = mock.return_address
    return_content_type = mock.return_content_type

    if return_content_type == 'application/json':
        callback_header = {'Content-type': str(return_content_type)}
        callback = requests.post(callback_api, data=json.dumps(data.json()), headers=callback_header)
        return callback.status_code


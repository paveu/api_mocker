import logging
from requests import request

from apimocker import task
from .enums import HTTP_METHODS

logger = logging.getLogger(__name__)


@task
def make_http_request(url, requested_http_method, requested_content_type, data=None):
    logger.info("mocker:make-http-request", extra={
        'url': url,
        'requested_http_method': requested_http_method,
        'requested_content_type': requested_content_type,
    })
    ret_data = None
    ret_json = None

    if data:
        if data.status_code != 200:
            ret_data = data.reason
        else:
            ret_data = data.text
            ret_json = data.json

    kw = {
        'data': ret_data,
        'json': ret_json,
        'params': None,
        'headers': {'Content-type': requested_content_type},
        'allow_redirects': False,
    }
    if kw in [HTTP_METHODS.POST, HTTP_METHODS.PUT, HTTP_METHODS.DELETE]:
        kw['allow_redirects'] = True
    return request(requested_http_method, url, **kw)

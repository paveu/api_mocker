import logging

from apimocker import task

logger = logging.getLogger(__name__)


@task
def hello():
    return 'hello world'

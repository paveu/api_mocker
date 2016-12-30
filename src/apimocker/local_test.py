from base import *
import dj_database_url

##### test
INSTALLED_APPS += (
    'django_nose',
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--nologcapture',
    '-s',
    '--tests=mocker_tests',
]
DATABASE_URL = 'postgres://ubuntu:@localhost/circle_test'
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}
# DATABASES['default']['OPTIONS'] = {
#     'autocommit': True,
# }

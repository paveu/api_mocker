from base import *

HOSTNAME = 'http://localhost:8000'
DATABASE_URL = "postgres://postgres:@localhost/mocker1_dev"
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}
# DATABASES['default']['OPTIONS'] = {
#     'autocommit': True,
# }

import sys
import dj_database_url

if 'collectstatic' not in ''.join(sys.argv):
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_MOCKER_URL)
    }

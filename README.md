## Installation

```
pip install -r requirements.txt
cd src
python manage.py migrate --fake-initial
python manage.py collectstatic --noinput
python manage.py createsu # you will get superadmin account with login: admin and pw: admin 
python manage.py runserver 0.0.0.0:8080 --settings=apimocker.settings_local # for running it locally
```

## Configuration

Files: 'src/apimocker/settings.py' and 'settings_local.py' contain HOSTNAME variable. This variable must reflect hostname used to host the project itself.
The hostname variable is used for creating Mocked API so it must be correct.


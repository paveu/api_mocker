## TODO
- add to form httpresponse fields
- fix remembering its url after clicking at it
(https://stackoverflow.com/questions/6366589/how-to-change-the-url-using-django-process-request)
(https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpResponseRedirect)
- remove static files from projects
- move devops folder to external repo
- make it as a pip package
- add sentry


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


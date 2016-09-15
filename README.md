## Installation

```
pip install -r requirements.txt
cd src
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsu # you will get superadmin account with login: admin and pw: admin 
python manage.py runserver 0.0.0.0:8080 --settings=apimocker.settings_local
```
FROM paveu/base-webapp

ENV APP_NAME apimocker
ENV CELERY_APP apimocker
ENV DJANGO_SETTINGS_MODULE apimocker.settings

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

WORKDIR /app
ADD . /app/

RUN ENVIRONMENT=production python manage.py collectstatic --no-input --link -v 0
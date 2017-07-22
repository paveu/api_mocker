FROM paveu/base-webapp

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash && apt-get install -y nodejs && apt-get install -y build-essential

ENV APP_NAME apimocker
ENV CELERY_APP apimocker
ENV DJANGO_SETTINGS_MODULE apimocker.settings

ADD /requirements/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

WORKDIR /app
ADD . /app/

RUN cd frontend && npm install webpack -g && npm install && npm rebuild node-sass && npm run build

RUN ENVIRONMENT=production python manage.py collectstatic --no-input --link -v 0

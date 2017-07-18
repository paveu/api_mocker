# API Mocker

[![N|Solid](https://circleci.com/gh/paveu/api_mocker/tree/develop.svg?style=shield&circle-token=fefd1e0b319193750fb2dc1a545cca97ddba350c)](https://github.com/paveu/api_mocker)

API Mocker is a Django powered API mock application. It can hide original API from 3rd party people.

# Features

  - Setting and limiting HTTP Content-types along with their methods for a mocked API.
  - API PUSH Callbacks. In case of an error or success it can return callback message(push) to defined client address. Push messages are sent asynchronous.
  - API content responses are stored in database.

### Tech

API Mocker uses a number of open source projects to work properly:

* [Django](https://www.djangoproject.com/) - free and open-source Python web framework.
* [Celery](http://www.celeryproject.org/) - open source asynchronous task queue or job queue which is based on distributed message passing.
* [Requests](http://docs.python-requests.org/en/master/) - Python HTTP library, released under the Apache2 License.
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) - Django application that lets you easily build, customize and reuse forms using your favorite CSS framework, without writing template code and without having to take care of annoying details.
* [Bootstrap](https://getbootstrap.com/) - great UI boilerplate for modern web apps
* [Sentry](https://sentry.io/) - real-time error tracking gives you insight into production deployments and information to reproduce and fix crashes.


### Development

Want to contribute? Great!. Pull requests are welcome!

### Todos

 - Save response headers to database
 - Add timeout for requests within mocker model
 - Save cookies to database if exist
 - Add webpack
 - Add REST endpoints
 - Logging to file or Kibana
 - Check if Event Hooks could be used as a replacement of implemented callbacks
 - Check if all requests could be done based on requests.Session()
 - Add allow_redirecation flag to mocker model
 - Add to form http response fields
 - Body Content Workflow with streams ?
 - Fix remembering its url after clicking at it (https://stackoverflow.com/questions/6366589/how-to-change-the-url-using-django-process-request), (https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpResponseRedirect)


License
----

MIT

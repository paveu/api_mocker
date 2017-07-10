# API Mocker

[![N|Solid](https://circleci.com/gh/paveu/api_mocker/tree/master.svg?style=shield&circle-token=fefd1e0b319193750fb2dc1a545cca97ddba350c)](https://github.com/paveu/api_mocker)

API Mocker is a Django powered API mock application. It can protect and hide your API from 3rd party people.

# Features

  - Possibility to mock and protect HTTP address.
  - API Callbacks. In case of an error or success it can return callback message(push) to defined client address. Push messages are sent asynchronous.
  - Defining return HTTP Content-Type along with HTTP sttus codes that could be used for mocked API.
  - All API call logs are stored in database.

### Tech

API Mocker uses a number of open source projects to work properly:

* [Django](https://www.djangoproject.com/) - free and open-source Python web framework.
* [Celery](http://www.celeryproject.org/) - open source asynchronous task queue or job queue which is based on distributed message passing.
* [Requests](http://docs.python-requests.org/en/master/) - Python HTTP library, released under the Apache2 License.
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) - Django application that lets you easily build, customize and reuse forms using your favorite CSS framework, without writing template code and without having to take care of annoying details.
* [Bootstrap](https://getbootstrap.com/) - great UI boilerplate for modern web apps


### Development

Want to contribute? Great!. Pull requests are welcome!

### Todos

 - Save response headers in APILog model
 - Check if Event Hooks could be used as a replace of implemented callbacks
 - Save cookies in APILog
 - Check if all requests could be done based on requests.Session()
 - Add allow_redirecation flag to mocker model
 - Add timeout for requests within mocker model
 - Add to form http response fields
 - Body Content Workflow with streams ?
 - Fix remembering its url after clicking at it (https://stackoverflow.com/questions/6366589/how-to-change-the-url-using-django-process-request), (https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpResponseRedirect)
 - Add http server to tests


License
----

MIT

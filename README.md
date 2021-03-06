# API Mocker

[![N|Solid](https://circleci.com/gh/paveu/api_mocker/tree/develop.svg?style=shield&circle-token=fefd1e0b319193750fb2dc1a545cca97ddba350c)](https://github.com/paveu/api_mocker)

API Mocker is a Django powered API proxy mock service

# Features

  - Mock your JSON API
  - Add custom headers
  - Push response callback
  - Record API response content and header in database
  - Supports for POST/GET/PATCH/PUT/DELETE/HEAD/OPTIONS http methods
  - Set your own response status code


### Tech

API Mocker uses a number of open source projects to work properly:

* [Django](https://www.djangoproject.com/) - free and open-source Python web framework.
* [Docker - Swarm mode](https://www.docker.com/) - open platform for developers and sysadmins to build, ship, and run distributed applications, whether on laptops, data center VMs, or the cloud.
* [Traefik](https://traefik.io/) - a modern HTTP reverse proxy and load balancer made to deploy microservices with ease.
* [ELK stack](https://www.elastic.co/webinars/introduction-elk-stack) - a collection of three open-source products: Elasticsearch, Logstash, and Kibana. Elasticsearch is a NoSQL database that is based on the Lucene search engine. Logstash is a log pipeline tool that accepts inputs from various sources, executes different transformations, and exports the data to various targets. Kibana is a visualization layer that works on top of Elasticsearch.
* [webpack](https://webpack.github.io/) - webpack is a module bundler this means webpack takes modules with dependencies and emits static assets representing those modules.
* [Celery](http://www.celeryproject.org/) - open source asynchronous task queue or job queue which is based on distributed message passing.
* [Requests](http://docs.python-requests.org/en/master/) - Python HTTP library, released under the Apache2 License.
* [Sentry](https://sentry.io/) - real-time error tracking gives you insight into production deployments and information to reproduce and fix crashes.
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) - Django application that lets you easily build, customize and reuse forms using your favorite CSS framework, without writing template code and without having to take care of annoying details.
* [Bootstrap](https://getbootstrap.com/) - great UI boilerplate for modern web apps


### Development

Want to contribute? Great!. Pull requests are welcome!


License
----

MIT

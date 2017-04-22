#!/bin/bash

docker-compose stop
# remove stopped containers
docker rm $(docker ps -a | grep Exited | awk '{print $1;}')
# or, to remove the stopped containers that were started by Docker Compose
docker rm $(docker ps -aq)
# sudo rm /var/lib/docker/network/files/local-kv.db

docker-compose rm
# remove untagged images

docker images -a -f dangling=true
docker rmi $(docker images -aq -f dangling=true)
docker rmi $(docker images -q --filter "dangling=true")
docker volume rm $(docker volume ls -f dangling=true -q)

# Better yet, remove dangling volumes before they're created by using -v
docker-compose rm -v


# docker-compose build
# docker-compose up -d
# docker-compose run web python manage.py migrate
# docker-compose run web /usr/local/bin/python manage.py migrate

# docker-machine ip dev
# curl $(boot2docker ip):8000



# docker volume create --name pgdata
# docker run -d -v pgdata:/var/lib/postgresql/data/ postgres
# docker exec -it mocker_db_1 psql -U postgres -c "CREATE DATABASE mocker1_dev;"

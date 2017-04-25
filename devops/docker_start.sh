## Build your whole Docker Compose project...
docker-compose build
## ...or just build one piece of it
#docker-compose build [app|db|etc...]

## Start your Docker Compose project
docker-compose up -d
## View the logs for this docker-compose project
#docker-compose logs
## Stop running containers
#docker-compose stop


# docker-compose build
# docker-compose up -d
# docker-compose run web python manage.py migrate
# docker-compose run web /usr/local/bin/python manage.py migrate

# docker-machine ip dev
# curl $(boot2docker ip):8000

# docker volume create --name pgdata
# docker run -d -v pgdata:/var/lib/postgresql/data/ postgres
# docker exec -it mocker_db_1 psql -U postgres -c "CREATE DATABASE mocker1_dev;"
#!/bin/bash

# Remove stopped containers
docker rm $(docker ps -a | grep Exited | awk '{print $1;}')

# Clean up un-tagged docker images
docker rmi $(docker images -q --filter "dangling=true")

# Stop and remove all containers (including running containers!)
docker rm -f $(docker ps -a -q)

# Stops running containers without removing them
docker-compose stop

# Remove the stopped containers that were started by Docker Compose.
# Anonymous volumes attached to containers will be removed
docker-compose rm -v

# docker images -a -f dangling=true
# docker rmi $(docker images -aq -f dangling=true)
# docker volume rm $(docker volume ls -f dangling=true -q)

# or, to remove the stopped containers that were started by Docker Compose
#docker rm $(docker ps -aq)
# sudo rm /var/lib/docker/network/files/local-kv.db


#!/bin/bash

BRANCH=$(git symbolic-ref --short -q HEAD);
SHA=$(git rev-parse HEAD);
PREFIX='local-'
VERSION=${PREFIX}${BRANCH}-${SHA:0:7}

IMAGE=paveu/apimocker

docker build -t ${IMAGE}:${VERSION} . | tee build.log || exit 1
ID=$(tail -1 build.log | awk '{print $3;}')
docker tag $ID ${IMAGE}:latest
docker images | grep ${IMAGE}

docker push ${IMAGE}:$ID
docker push ${IMAGE}:latest

docker system prune --force

### Swarm - Master node (manager)
# docker-machine env default
# eval $(docker-machine env default)
# docker-machine ssh default "docker node ls"

## Recreate Swarm
# docker-machine ssh default sudo sysctl -w vm.max_map_count=262144
# docker-machine ssh default "docker swarm leave --force"
# docker-machine ssh default "docker swarm init --advertise-addr 192.168.99.100"

# docker-machine ssh myvm1 "docker swarm leave --force"
# docker-machine ssh myvm1 "docker swarm join --token SWMTKN-1-0ft3r53r1p5804e66hq51pg9da06f4q4aolzbtbm8w2h4fhm82-dbgyct49kph32vlnx7gdyn0we 192.168.99.100:2377"
# docker-machine ssh myvm1 sudo sysctl -w vm.max_map_count=262144

# docker-machine ssh myvm2 "docker swarm leave --force"
# docker-machine ssh myvm2 "docker swarm join --token SWMTKN-1-2n3bhmylapbxm6wln0ictczpgka7bmr6rfvtsnymcteqorewxg-bbekj5nyro2yc6tkfrow7plkc 192.168.99.100:2377"
# docker-machine ssh myvm2 sudo sysctl -w vm.max_map_count=262144

### Remove and deploy stack
# docker stack rm getstartedlab
# docker stack deploy -c docker-compose.yml getstartedlab

### After we make change to compose file we can updated all services by running
# docker stack deploy -c docker-compose.yml getstartedlab

### New image scenario
# Step 1) build this script
# Step 2) docker service update --force getstartedlab_web

### Scale services -> 'getstartedlab_web' service
# docker service ls
# docker service scale getstartedlab_web=3

### Service inspection
# docker stack ps getstartedlab # stack visuaalization
# docker stack services getstartedlab
# docker service inspect getstartedlab_web
# docker service ps getstartedlab_web
# docker service logs getstartedlab_web --details -t
# docker container ls
# docker stats --all

### Container process usage
# docker container ls
# docker top 832e03dbf971

### Image rollback scenario
# https://gist.github.com/paveu/72316344639eb03ec57047f62305107e

### Log in to docker container
# >$ docker ps
# CONTAINER ID        IMAGE             COMMAND                  CREATED             STATUS              PORTS               NAMES
# e53bff8bebfc        login-arm64:1.0   "/bin/sh -c 'node ser"   27 seconds ago      Up 25 seconds                           login.1.cg7fltcu3wfe7ixtnqzg8myy1
#
# >$ docker exec -it c30d4e94f5e4 bash
# root@e53bff8bebfc:/#

####################################
#### Other commands reference ######
####################################
#docker build -t friendlyname .  # Create image using this directory's Dockerfile
#docker run -p 4000:80 friendlyname  # Run "friendlyname" mapping port 4000 to 80
#docker run -d -p 4000:80 friendlyname         # Same thing, but in detached mode
#docker container ls                                # List all running containers
#docker container ls -a             # List all containers, even those not running
#docker container stop <hash>           # Gracefully stop the specified container
#docker container kill <hash>         # Force shutdown of the specified container
#docker container rm <hash>        # Remove specified container from this machine
#docker container rm $(docker container ls -a -q)         # Remove all containers
#docker image ls -a                             # List all images on this machine
#docker image rm <image id>            # Remove specified image from this machine
#docker image rm $(docker image ls -a -q)   # Remove all images from this machine
#docker login             # Log in this CLI session using your Docker credentials
#docker tag <image> username/repository:tag  # Tag <image> for upload to registry
#docker push username/repository:tag            # Upload tagged image to registry
#docker run username/repository:tag                   # Run image from a registry

#docker stack ls                                            # List stacks or apps
#docker stack deploy -c <composefile> <appname>  # Run the specified Compose file
#docker service ls                 # List running services associated with an app
#docker service ps <service>                  # List tasks associated with an app
#docker inspect <task or container>                   # Inspect task or container
#docker container ls -q                                      # List container IDs
#docker stack rm <appname>                             # Tear down an application

#docker-machine create --driver virtualbox myvm1 # Create a VM (Mac, Win7, Linux)
#docker-machine create -d hyperv --hyperv-virtual-switch "myswitch" myvm1 # Win10
#docker-machine env myvm1                # View basic information about your node
#docker-machine ssh myvm1 "docker node ls"         # List the nodes in your swarm
#docker-machine ssh myvm1 "docker node inspect <node ID>"        # Inspect a node
#docker-machine ssh myvm1 "docker swarm join-token -q worker"   # View join token
#docker-machine ssh myvm1   # Open an SSH session with the VM; type "exit" to end
#docker-machine ssh myvm2 "docker swarm leave"  # Make the worker leave the swarm
#docker-machine ssh myvm1 "docker swarm leave -f" # Make master leave, kill swarm
#docker-machine start myvm1            # Start a VM that is currently not running
#docker-machine stop $(docker-machine ls -q)               # Stop all running VMs
#docker-machine rm $(docker-machine ls -q) # Delete all VMs and their disk images
#docker-machine scp docker-compose.yml myvm1:~     # Copy file to node's home dir
#docker-machine ssh myvm1 "docker stack deploy -c <file> <app>"   # Deploy an app
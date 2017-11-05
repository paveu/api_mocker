#!/bin/bash

BRANCH=$(git symbolic-ref --short -q HEAD);
SHA=$(git rev-parse HEAD);
PREFIX='local-'
VERSION=${PREFIX}${BRANCH}-${SHA:0:7}

IMAGE=paveu/apimocker

docker build -t ${IMAGE}:${VERSION} . | tee build.log || exit 1
ID=$(tail -1 build.log | awk '{print $3;}')
docker tag $ID ${IMAGE}:${SHA:0:7}
docker tag $ID ${IMAGE}:latest
docker images | grep ${IMAGE}

docker push ${IMAGE}:${SHA:0:7}
docker push ${IMAGE}:latest

docker system prune --force

##### Digital Ocean docker machine ######
#    export DIGITALOCEAN_ACCESS_TOKEN=""
#    export DIGITALOCEAN_IMAGE="ubuntu-16-04-x64"
#    export DIGITALOCEAN_REGION="fra1"
#    export DIGITALOCEAN_SIZE="4gb"
#    export DIGITALOCEAN_PRIVATE_NETWORKING="true"
#    export DIGITALOCEAN_IPV6="true"
#    docker-machine create --driver digitalocean --digitalocean-image $DIGITALOCEAN_IMAGE --digitalocean-region $DIGITALOCEAN_REGION --digitalocean-size $DIGITALOCEAN_SIZE --digitalocean-ipv6 --digitalocean-private-networking managerprod
#    eval $(docker-machine env managerprod)
#    docker-machine ssh managerprod "docker swarm init --listen-addr $(docker-machine ip managerprod) --advertise-addr $(docker-machine ip managerprod)"
#    docker network create --driver overlay frontend
#    docker-machine ssh managerprod sudo sysctl -w vm.max_map_count=262144
#    docker stack deploy balancer -c stack/prod_balancer.yml
#    docker stack deploy ops -c stack/prod_ops.yml
#    docker stack deploy app -c stack/prod_app.yml

##### Configure Swarm Mode Cluster - locally
### Create Manager machine with at least 2GB RAM!!!!!!!! It is needed for ELK stack (Kibana)
# docker-machine create -d managerlocal
# docker-machine create -d virtualbox worker1
# eval $(docker-machine env managerlocal)

# Leave Swarm mode if they joined in
# docker-machine ssh managerlocal "docker swarm leave --force"
# docker-machine ssh worker1 "docker swarm leave --force"
# docker-machine ssh worker2 "docker swarm leave --force"

# docker-machine ssh managerlocal "docker swarm init --listen-addr $(docker-machine ip managerlocal) --advertise-addr $(docker-machine ip managerlocal)"
# export worker_token=$(docker-machine ssh managerlocal "docker swarm join-token worker -q")
# docker-machine ssh worker1 "docker swarm join --token=${worker_token} --listen-addr $(docker-machine ip worker1) --advertise-addr $(docker-machine ip worker1) $(docker-machine ip managerlocal)"
# docker-machine ssh worker2 "docker swarm join --token=${worker_token} --listen-addr $(docker-machine ip worker2) --advertise-addr $(docker-machine ip worker2) $(docker-machine ip managerlocal)"
# docker-machine ssh managerlocal "docker node ls"

# Create network for Swarm Cluster
# docker network create --driver overlay frontend

#### Set new max_map_count value for ELK
# docker-machine ssh managerlocal sudo sysctl -w vm.max_map_count=262144
# docker-machine ssh worker1 sudo sysctl -w vm.max_map_count=262144
# docker-machine ssh worker2 sudo sysctl -w vm.max_map_count=262144

### create new stack locally
# docker stack deploy balancer -c stack/local_balancer.yml
# docker stack deploy ops -c stack/local_ops.yml
# docker stack deploy app -c stack/local_app.yml

### Remove new stack
# docker stack rm balancer
# docker stack rm ops
# docker stack rm app

### New image scenario
# Step 1) build this image
# Step 2) docker service update --force app_web

### Scale services -> 'app_web' service
# docker service ls
# docker service scale app_web=3

### Service inspection
# docker stack ps app_web # stack visuaalization
# docker stack services app_web
# docker service inspect app_web
# docker service ps app_web
# docker service logs app_web --details -t
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

############ Swarm Mode Cluster configuration - local
### Debug - in case of CA problems with docker-machines
# unset ${!DOCKER*}

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
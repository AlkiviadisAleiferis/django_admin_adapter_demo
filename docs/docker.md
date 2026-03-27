## Docker {UNI}INSTALLATION PROCESS:

https://docs.docker.com/engine/install/ubuntu/

----------------------------------------------------------
### find installed docker (if installed):
```dpkg -l | grep -i docker```



----------------------------------------------------------
## INSTALL + UNINSTALL
https://docs.docker.com/engine/install/ubuntu/


----------------------------------------------------------
### total uninstall:
``` for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove --purge $pkg; done```

The unofficial packages to uninstall are:

- docker.io
- docker-compose
- docker-compose-v2
- docker-doc
- podman-docker


----------------------------------------------------------
### List the available versions:
```apt-cache madison docker-ce | awk '{ print $3 }'```

e.g. 5:24.0.9-1~ubuntu.23.04~lunar

```VERSION_STRING=5:24.0.9-1~ubuntu.22.04~jammy```
```VERSION_STRING=5:26.1.4-1~ubuntu.22.04~jammy```
```sudo apt-get install -y docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin```



----------------------------------------------------------
### Hold update of docker package:

WARNING: SET `sudo apt-mark hold docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin` to avoid automatic upgrade
Add the docker group (it might be already exist):
```sudo groupadd docker```



----------------------------------------------------------
### Add the connected user “$USER” to the docker group:
```sudo gpasswd -a $USER docker```

Either do a newgrp docker or log out/in to activate the changes to groups:
```newgrp docker```

Run docker run hello-world command to test it:
```docker run hello-world```



----------------------------------------------------------
### total docker system reboot:

```
docker container rm -f $(docker container ls -qa)
docker volume rm -f $(docker volume ls -q)
docker image rm -f $(docker image ls -aq)
docker network rm -f $(docker network ls -q)
docker system prune
docker buildx prune
```



----------------------------------------------------------
### Useful commands/configs:

remove everything:
`docker  system prune --volumes -af`

show docker disk usage:
`docker  system df`

remove build cache:
`docker buildx prune`

configure docker from `/etc/docker/daemon.json`



----------------------------------------------------------
### Docker permissions:

1. Create the docker group.
`sudo groupadd docker`
2. Add your user to the docker group.
`sudo usermod -aG docker $USER`
3. Log out and log back in so that your group membership is re-evaluated.
If you're running Linux in a virtual machine,
it may be necessary to restart the virtual
machine for changes to take effect.

You can also run the following command to activate the changes to groups:
`newgrp docker`



----------------------------------------------------------
### deployment

CURRENT_VERSION = 5:24.0.9-1~ubuntu.22.04~jammy

building images with:
`docker compose build --no-cache`

keep track of containers:
`docker stats --all` + `watch -d docker ps -a`

remove older images with: `rm -f --remove-orphans` or `docker load < image.tar`

load image from .tar file with `docker load --input fedora.tar`



----------------------------------------------------------
### Docker compose.yaml file specified

use `COMPOSE_FILE` envorinment variable to specify production `compose.production.yaml`

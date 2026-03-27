## DEPLOYMENT PROCESS



### Create system user

`useradd -r -u 444 -d /opt -s /bin/bash username`

`usermod -aG sudo username`

`passwd username` # provide pass

`su username`



----------------------------------------------------------
### Generate SSH keys

Run `ssh-keygen` and follow instructions (dont change directory and probably dont give passphrase)



----------------------------------------------------------
### Install ssh keys on server

- `sudo mkdir -p /opt/.ssh`

- `sudo chown username /opt/.ssh`

- `cd /opt/.ssh && touch authorized_keys`

- from sys admin machine: `ssh-copy-id -i ~/.ssh/id_rsa.pub username@host`



----------------------------------------------------------
### use ssh to connect to remote machine

`ssh username@host`


----------------------------------------------------------
### Disable root access


----------------------------------------------------------
### change ssh port



----------------------------------------------------------
### Install proper docker version and document it

see correspoonding doc file



----------------------------------------------------------
### Create docker group and add system user to it

- `sudo usermod -aG docker username` OR `sudo gpasswd -a $USER docker`
- `newgrp docker`
- `sudo reboot`



----------------------------------------------------------
### Docker check service and enable if not enabled

- `sudo systemctl status docker.service`
- `sudo systemctl enable docker.service`



----------------------------------------------------------
### Create project's folder:

`sudo mkdir -p /opt/project_name && sudo chown username /opt/project_name`

automatic if git cloned



----------------------------------------------------------
### Retrieve project from VC

CAREFUL authenticate with

`BROWSER=false gh auth login`

clone git repository

`git clone vc_url`



----------------------------------------------------------
### create data directories

```
cd /opt/django_admin_adapter_demo && \
mkdir -p data/db/dumps && \
mkdir -p data/admin_api/media/files && \
mkdir -p data/admin_api/media/images && \
mkdir -p data/admin_api/static && \
mkdir -p data/logging/admin_api && \
mkdir -p data/logging/nginx && \
mkdir -p data/redis
```


----------------------------------------------------------
### create NGINX certificates

`cd /opt/asset_manage/docker/production/nginx`
`sudo openssl req -x509 -nodes --trustout -sha256 -days 3650 -newkey rsa:4096 -keyout ./nginx-selfsigned.key -out ./nginx-selfsigned.crt`

`sudo openssl dhparam -out ./dhparam.pem 2048`

`cd ./docker/production/nginx`

`
sudo chown username nginx-selfsigned.crt && sudo chmod 600 username nginx-selfsigned.crt && \
sudo chown username nginx-selfsigned.key && sudo chmod 600 username nginx-selfsigned.key && \
sudo chown username dhparam.pem && sudo chmod 600 username dhparam.pem
`


----------------------------------------------------------
### Copy necessary non git versioned files (certificates/other files)
`cd /opt/asset_manage/docker/production/redis`
`redis_pass='password'`

create users.acl
`printf "user asset_manage_admin on >${redis_pass} "'~* &* +@'"all\nuser default on>${redis_pass}" > users.acl`
`sudo chown root users.acl`

create redis.conf
`printf "user asset_manage_admin on >${redis_pass}"' ~* &* +@all'"\nuser default on >${redis_pass}\nappendonly yes\ndbfilename REDIS_DB_FILE.rdb" > redis.conf`
`sudo chown root redis.conf`

`scp ./.env username@${SERVER_IP}:/opt/asset_manage`



----------------------------------------------------------
### initialize db --> create superusers/groups/permissions

run while containers are up:

`docker compose exec admin_api python3 manage.py init_db`

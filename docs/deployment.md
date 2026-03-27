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
sudo chown salpix nginx-selfsigned.crt && sudo chmod 600 salpix nginx-selfsigned.crt && \
sudo chown salpix nginx-selfsigned.key && sudo chmod 600 salpix nginx-selfsigned.key && \
sudo chown salpix dhparam.pem && sudo chmod 600 salpix dhparam.pem
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

`scp ./.env salpix@${SERVER_IP}:/opt/asset_manage`



----------------------------------------------------------
### build services with no cache



----------------------------------------------------------
### Up containers



----------------------------------------------------------
### install fixtures common: country,city,bank. issues:labels, chatgen:document_type and create superuser
`docker compose exec infosys python3 manage.py loaddata backend/fixtures/common/country.json`
`docker compose exec infosys python3 manage.py loaddata backend/fixtures/common/city.json`
`docker compose exec infosys python3 manage.py loaddata backend/fixtures/common/bank.json`
`docker compose exec infosys python3 manage.py loaddata backend/fixtures/chatgen/document_type.json`
`docker compose exec infosys python3 manage.py install_administration_permissions`



----------------------------------------------------------
### create superusers/groups/permissions


----------------------------------------------------------
### Set up cron job for db dump
cron job for data dump:
min hr months days weekdays command
dev:
`30 22 1-31 1-12 0-6 cd /home/alkis/PROJECTS/salpix/salpix && docker compose exec db pg_dump -U asset_manage_admin -d salpix_asset_manage -f /opt/PGDUMP2.sql`
prod:
`00 00 1-31 1-12 0-6 cd /opt/asset_manage && docker compose exec db pg_dump -U asset_manage_admin -d salpix_asset_manage -f /opt/PGDUMP1.sql && docker compose exec db chown salpix /opt/PGDUMP1.sql`

`00 12 1-31 1-12 0-6 cd /opt/asset_manage && docker compose exec db pg_dump -U asset_manage_admin -d salpix_asset_manage -f /opt/PGDUMP2.sql && docker compose exec db chown salpix /opt/PGDUMP2.sql`

backup dump file locally:
`scp salpix@${SERVER_IP}:/opt/asset_manage/data/db/dumps/PGDUMP.sql ~/salpix/db_dumps`



----------------------------------------------------------
#### set up VM's ENV vars
set up /opt/.profile
```
export PROJECT_HOST_BASE_DIR='/opr/asset_manage'
export DROPBOX_REFRESH_TOKEN='redresh_token'
export DROPBOX_APP_KEY='app_key'
export DROPBOX_APP_SECRET='app_secret'
```

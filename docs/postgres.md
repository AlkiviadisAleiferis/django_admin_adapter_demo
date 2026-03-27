# POSTGRES:

## WARNING:
In host machine install **python3.11-dev**, or `psycopg2` install will raise error

## Install pgadmin in ubuntu 22.04:
  `curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add`
  `sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/focal/ pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'`
  `sudo apt install pgadmin4-desktop`

`docker compose exec db bash`

## interactive postgre shell:
  `psql -U django_admin_adapter_admin  -d django_admin_adapter`

## change db password:
  `ALTER USER django_admin_adapter_admin WITH PASSWORD 'newpass';`

## In Psql you could run commands such as:
  `\?` list all the commands
  `\l` list databases
  `\conninfo` display information about current connection
  `\c [DBNAME]` connect to new database, e.g., \c template1
  `\dt` list tables of the public schema
  `\dt <schema-name>.*` list tables of certain schema, e.g., \dt public.*
  `\dt *.*` list tables of all schemas
  `\q` quit psql

## PG dump database:
  `pg_dump -U django_admin_adapter_admin -d django_admin_adapter -f /opt/PGDUMP.sql`

## PG restore db:
`psql -U django_admin_adapter_admin -d django_admin_adapter < /opt/PGDUMP.sql`

## cron job for data dump:

min hr months days weekdays command
dev:
  `30 22 1-31 1-12 0-6 cd /home/alkis/PROJECTS/ayioncore/ayioncore && docker compose exec db pg_dump -U django_admin_adapter_admin -d django_admin_adapter -f /opt/PGDUMP2.sql`
prod:
  `00 00 1-31 1-12 0-6 cd /opt/asset_manage && docker compose exec db pg_dump -U django_admin_adapter_admin -d django_admin_adapter -f /opt/asset_manage/data/dumps/PGDUMP1.sql`
  `00 12 1-31 1-12 0-6 cd /opt/asset_manage && docker compose exec db pg_dump -U django_admin_adapter_admin -d django_admin_adapter -f /opt/asset_manage/data/dumps/PGDUMP2.sql`

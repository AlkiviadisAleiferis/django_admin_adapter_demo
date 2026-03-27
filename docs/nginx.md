#                 NGINX:

### Create certificates:
  `cd /opt/asset_manage`
  `sudo openssl req -x509 -nodes --trustout -sha256 -days 730 -newkey rsa:4096 -keyout ./docker/production/nginx/nginx-selfsigned.key -out ./docker/production/nginx/nginx-selfsigned.crt`
  `sudo openssl dhparam -out ./docker/production/nginx/dhparam.pem 2048`

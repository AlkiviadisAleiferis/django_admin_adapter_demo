valid video URL for setting certificate with Let's encrypt
https://www.youtube.com/watch?v=bwYZ1yCHaFw&ab_channel=WittCode

install certbot : `sudo apt install certbot`

make sure port 80 is free

run `certbot certonly --standalone -d domain.com`

certificates will be in `/etc/letsencrypt/live/domain.com`

`fullchain.pem` is the public key and `privkey.pem` is the private key

rename and copy those certificates to `/opt/cert/docker/nginx/production/cert.crt + cert.key`

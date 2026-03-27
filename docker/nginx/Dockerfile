FROM ubuntu:22.04 AS nginx_base

ARG BUILD_TARGET
ARG DOCKER_USER
ARG DOCKER_USER_ID

ARG ADMIN_API_STATIC_ROOT
ARG ADMIN_API_MEDIA_ROOT

RUN useradd -r -u ${DOCKER_USER_ID} -d /opt -s /bin/bash ${DOCKER_USER}
RUN usermod -aG sudo ${DOCKER_USER}

RUN apt-get update && apt-get install -y nginx-light systemctl

RUN rm /etc/logrotate.d/nginx
RUN rm /etc/nginx/nginx.conf

COPY --chown=${DOCKER_USER}:${DOCKER_USER} ./docker/nginx/nginx /etc/logrotate.d/

RUN rm /etc/nginx/sites-enabled/default

RUN mkdir -p ${ADMIN_API_STATIC_ROOT}  && chown ${DOCKER_USER}:${DOCKER_USER} ${ADMIN_API_STATIC_ROOT} && chmod 660 ${ADMIN_API_STATIC_ROOT}
# must be removed to integrate S3 object storage
RUN mkdir -p ${ADMIN_API_MEDIA_ROOT}  && chown ${DOCKER_USER}:${DOCKER_USER} ${ADMIN_API_MEDIA_ROOT} && chmod 660 ${ADMIN_API_MEDIA_ROOT}

RUN chown -R ${DOCKER_USER} /var/lib/nginx
RUN touch /run/nginx.pid && chown ${DOCKER_USER} /run/nginx.pid

EXPOSE 80

COPY --chown=${DOCKER_USER}:${DOCKER_USER} ./docker/nginx/${BUILD_TARGET}/nginx.conf /etc/nginx/
COPY --chown=${DOCKER_USER}:${DOCKER_USER} ./docker/nginx/${BUILD_TARGET}/cert.crt /etc/ssl/certs/cert.crt
COPY --chown=${DOCKER_USER}:${DOCKER_USER} ./docker/nginx/${BUILD_TARGET}/cert.key /etc/ssl/private/cert.key
COPY --chown=${DOCKER_USER}:${DOCKER_USER} ./docker/nginx/${BUILD_TARGET}/dhparam.pem /etc/nginx/ssl/dhparam.pem

USER ${DOCKER_USER}

CMD ["nginx", "-g", "daemon off;"]

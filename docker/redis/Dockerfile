FROM redis:7.2-bookworm

ARG BUILD_TARGET
ARG REDIS_PORT

RUN apt-get update && apt-get install -y redis-tools

ENV REDIS_ENV custom

EXPOSE $REDIS_PORT

COPY ./docker/redis/${BUILD_TARGET}/redis.conf /data
COPY ./docker/redis/${BUILD_TARGET}/users.acl /data

CMD ["redis-server", "/data/redis.conf"]

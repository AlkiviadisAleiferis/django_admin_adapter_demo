#!/bin/bash
until cd ${PROJECT_BASE_DIR}
do
    echo "Waiting for server volume..."
done

python3 ${PROJECT_BASE_DIR}/manage.py collectstatic --noinput

gunicorn wsgi:application --reload \
    --bind 0.0.0.0:$ADMIN_API_PORT \
    --workers 4 \
    --log-level INFO \
    # --capture-output \ best for production
    --log-level "debug" \
    --enable-stdio-inheritance \
    --log-file ${ADMIN_API_LOGGING_DIR}/gunicorn.log

#!/bin/sh
alembic upgrade head
exec gunicorn main:app -k uvicorn_settings.MyUvicornWorker --log-level $LOG_LEVEL
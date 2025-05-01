#!/bin/bash
sleep 7 && alembic upgrade head && gunicorn application.api.v1.app:get_app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


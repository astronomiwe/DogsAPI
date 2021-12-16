#!/bin/bash

# Frontend VARS
export DANGEROUSLY_DISABLE_HOST_CHECK=true

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations (if need)"
python manage.py migrate

# Starting autotests
# echo "starting autotests"
# python manage.py test

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000


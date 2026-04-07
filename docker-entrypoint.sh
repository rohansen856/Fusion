#!/bin/bash

set -e

# Apply database migrations
echo "Apply database migrations"
python FusionIIIT/manage.py makemigrations --noinput
python FusionIIIT/manage.py migrate --noinput

echo "Migrations completed successfully!"

# Start server
echo "Starting server"
python FusionIIIT/manage.py runserver 0.0.0.0:8000

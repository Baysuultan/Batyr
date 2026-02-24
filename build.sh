#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist (optional, for first deployment)
python manage.py createsuperuser --noinput --username admin --email admin@coursehub.kz 2>/dev/null || true

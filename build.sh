#!/usr/bin/env bash
# Render runs this as the build step (see render.yaml).
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

#!/usr/bin/env bash
# Render runs this as the build step (see render.yaml).
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_admin
# Content and plans -- all safe to re-run on every deploy.
python manage.py seed_plans
python manage.py seed_english_esl
python manage.py seed_workplace_english
python manage.py seed_school_english
python manage.py load_ielts_lesson ielts_content/
python manage.py seed_full_iq_test

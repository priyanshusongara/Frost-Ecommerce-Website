#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect Static Files
# The --clear flag ensures a fresh start on the Render server
python manage.py collectstatic --noinput --clear
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="admin@frost.com").exists():
    User.objects.create_superuser(
        "Admin",
        "User",
        "priyanshusongara23@gmail.com",
        "Priyanshu",
        "Radha@2002"
    )
EOF



#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput --clear
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



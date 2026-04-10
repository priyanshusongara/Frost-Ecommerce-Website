#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(email="admin@frost.com").exists():
    User.objects.create_superuser(
        "Admin",
        "User",
        "admin@frost.com",
        "admin",
        "admin123"
    )
EOF
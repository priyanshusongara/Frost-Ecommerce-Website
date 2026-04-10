#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="admin@example.com").exists():
    User.objects.create_superuser(
        "admin@example.com",
        "admin",
        "admin123"
    )
EOF
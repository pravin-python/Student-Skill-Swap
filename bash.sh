#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Run migrations
python manage.py makemigrations accounts, core, category_skills, university
python manage.py migrate
python manage.py demo_data

# Create superuser (agar chahiye to)
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

# Insert demo data into your apps


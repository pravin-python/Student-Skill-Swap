#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser (agar chahiye to)
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

# Insert demo data into your apps
echo "from apps.university.models import Country, State
if not Country.objects.filter(name='India').exists():
    india = Country.objects.create(name='India')
    State.objects.create(name='Gujarat', country=india)
    State.objects.create(name='Maharashtra', country=india)
print('✅ Demo data inserted')" | python manage.py shell


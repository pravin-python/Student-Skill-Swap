@echo off
REM Activate virtual environment
call .venv\Scripts\activate

REM Run migrations
python manage.py migrate

REM Insert demo data
python manage.py shell -c "from apps.university.models import Country, State; \
if not Country.objects.filter(name='India').exists(): \
    india = Country.objects.create(name='India'); \
    State.objects.create(name='Gujarat', country=india); \
    State.objects.create(name='Maharashtra', country=india); \
print('✅ Demo data inserted')"


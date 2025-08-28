@echo off
REM Activate virtual environment
call .venv\Scripts\activate

REM Run migrations
python manage.py makemigrations accounts, core, category_skills, university
python manage.py migrate
python manage.py demo_data


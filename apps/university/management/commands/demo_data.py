import os
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from apps.university.models import Country, State, City, University, UniversityImages, Department, Branch
from apps.category_skills.models import SkillsCategory, Skills

class Command(BaseCommand):
    help = 'Populate initial data for countries, states, cities, universities, departments, and branches'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data population...")

        # ----- Countries -----
        countries = []
        for i in range(1, 11):
            country, created = Country.objects.get_or_create(name=f"Country {i}")
            countries.append(country)
        self.stdout.write("Countries added.")

        # ----- States -----
        states = []
        for country in countries:
            for i in range(1, 11):
                state, created = State.objects.get_or_create(name=f"State {i} of {country.name}", country=country)
                states.append(state)
        self.stdout.write("States added.")

        # ----- Cities -----
        cities = []
        for state in states:
            for i in range(1, 11):
                city, created = City.objects.get_or_create(name=f"City {i} of {state.name}", state=state)
                cities.append(city)
        self.stdout.write("Cities added.")

        # ----- Universities -----
        image_folder = os.path.join(settings.BASE_DIR, 'static', 'assets', 'img', 'education')
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png','.jpg','.jpeg'))]

        universities = []

        for city in cities[:10]:
            for i in range(1, 11):
                image_path = os.path.join(image_folder, image_files[(i-1) % len(image_files)])
                with open(image_path, 'rb') as f:
                    django_file = File(f, name=image_files[(i-1) % len(image_files)])  # <- important
                    university, created = University.objects.get_or_create(
                        name=f"University {i} of {city.name}",
                        defaults={
                            'description': f"Description for University {i} in {city.name}",
                            'established_year': 2000 + i,
                            'country': city.state.country,
                            'state': city.state,
                            'city': city,
                            'image': django_file
                        }
                    )
                universities.append(university)

        # ----- Departments -----
        departments = []
        for i in range(1, 11):
            dept, created = Department.objects.get_or_create(
                name=f"Department {i}",
                defaults={'description': f"Description for Department {i}"}
            )
            departments.append(dept)
        self.stdout.write("Departments added.")

        # ----- Branches -----
        for dept in departments:
            for i in range(1, 11):
                Branch.objects.get_or_create(
                    name=f"Branch {i} of {dept.name}",
                    department=dept,
                    defaults={'description': f"Description for Branch {i} of {dept.name}"}
                )
        self.stdout.write("Branches added.")

        # ----- Categories -----
        category_data = {
            "Technology": ["Python", "Java", "Fullstack", "Django", "React"],
            "Design": ["Photoshop", "Figma", "Illustrator", "UI/UX", "Animation"],
            "Business": ["Marketing", "Finance", "Management", "Sales", "Analytics"],
        }

        # static images for categories
        image_folder = os.path.join(settings.BASE_DIR, 'static', 'assets', 'img', 'person')
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png','.jpg','.jpeg'))]

        categories = []
        for idx, (cat_name, skills_list) in enumerate(category_data.items()):
            image_path = os.path.join(image_folder, image_files[idx % len(image_files)])
            with open(image_path, 'rb') as f:
                django_file = File(f, name=image_files[idx % len(image_files)])
                category, created = SkillsCategory.objects.get_or_create(
                    name=cat_name,
                    defaults={
                        "description": f"{cat_name} related courses",
                        "image": django_file
                    }
                )
            categories.append(category)

            # ----- Skills for this category -----
            for skill_name in skills_list:
                Skills.objects.get_or_create(
                    name=skill_name,
                    category=category,
                    defaults={
                        "description": f"{skill_name} skill in {cat_name}"
                    }
                )

        self.stdout.write(self.style.SUCCESS("Data population completed successfully!"))

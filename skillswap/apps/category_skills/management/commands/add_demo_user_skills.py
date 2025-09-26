from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.category_skills.models import Skills, UserSkills
import random

class Command(BaseCommand):
    help = 'Add demo user skills for testing'

    def handle(self, *args, **options):
        # Get all users and skills
        users = User.objects.all()
        skills = Skills.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return
            
        if not skills.exists():
            self.stdout.write(self.style.ERROR('No skills found. Please create skills first.'))
            return
        
        # Add random skills to users
        added_count = 0
        for user in users:
            # Add 2-4 random skills to each user
            num_skills = random.randint(2, 4)
            user_skills = random.sample(list(skills), min(num_skills, len(skills)))
            
            for skill in user_skills:
                user_skill, created = UserSkills.objects.get_or_create(
                    user=user,
                    skill=skill
                )
                if created:
                    added_count += 1
                    self.stdout.write(f'Added skill "{skill.name}" to user "{user.username}"')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {added_count} user skills!')
        )

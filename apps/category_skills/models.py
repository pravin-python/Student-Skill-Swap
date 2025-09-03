from django.db import models
from apps.accounts.models import User
import os

class SkillsCategory(models.Model):

    class Meta:
        ordering = ['name']
        db_table = 'category'
        verbose_name_plural = "Skill Categories"

    name = models.CharField(max_length=25,unique=True)
    description = models.TextField(max_length=999,help_text="Enter Description For Particular Course")
    icon_class = models.CharField(max_length=50,blank=True,null=True)
    image = models.ImageField(upload_to='category/' , blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    

def category_skills(instance , filename):
        return os.path.join('category_skills', instance.category.name, filename)


class Skills(models.Model):

    class Meta:
        ordering = ['category' , 'name']
        db_table = 'category_skills'
        unique_together = ['name','category']
        verbose_name_plural = 'Skills'
    
    LEVEL_CHOICES = (
         ('B' , 'Beginner'),
         ('I' , 'Intermediate'),
         ('A' , 'Advanced'),
    )
    name = models.CharField(max_length=200,unique=True)
    category = models.ForeignKey(SkillsCategory,on_delete=models.CASCADE,related_name='skills')
    image = models.ImageField(upload_to=category_skills,blank=True,null=True)
    description = models.TextField(max_length=999,help_text="Enter Description for Specific Skill") 
    level = models.CharField(max_length=25 , choices=LEVEL_CHOICES , default='Beginner')
 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    


class UserSkills(models.Model):
  
    class Meta:
        db_table = 'user_skills'
        unique_together = ['user', 'skill']
        verbose_name_plural = 'User Skills'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='user_skills')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"


class Request(models.Model):

    REQUEST_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('C', 'Cancelled'),
    )

    class Meta:
        db_table = 'skill_requests'
        unique_together = ['requester', 'receiver', 'skill']
        verbose_name_plural = 'Skill Requests'
        ordering = ['-created_at']

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests', help_text="User who wants to learn the skill")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests', help_text="User who has the skill")
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='skill_requests')
    status = models.CharField(max_length=1, choices=REQUEST_STATUS_CHOICES, default='P')
    description = models.TextField(max_length=500, help_text="Message from requester to receiver")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(null=True, blank=True, help_text="When receiver responded to request")

    def __str__(self):
        return f"{self.requester.username} → {self.receiver.username} ({self.skill.name})"

    @property
    def status_display(self):
        return dict(self.REQUEST_STATUS_CHOICES)[self.status]


class Session(models.Model):

    SESSION_STATUS_CHOICES = (
        ('S', 'Scheduled'),
        ('A', 'Active'),
        ('C', 'Completed'),
        ('CA', 'Cancelled'),
        ('P', 'Pending'),
    )

    SESSION_TYPE_CHOICES = (
        ('O', 'Online'),
        ('I', 'In-Person'),
        ('H', 'Hybrid'),
    )

    class Meta:
        db_table = 'skill_sessions'
        verbose_name_plural = 'Skill Sessions'
        ordering = ['-created_at']

    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='sessions', help_text="Associated request")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_sessions')
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_sessions')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='skill_sessions')
    
    title = models.CharField(max_length=200, help_text="Session title")
    description = models.TextField(max_length=1000, blank=True, help_text="Session description and agenda")
    
    session_type = models.CharField(max_length=1, choices=SESSION_TYPE_CHOICES, default='O')
    location = models.CharField(max_length=300, blank=True, help_text="Meeting location or online platform")
    
    scheduled_date = models.DateTimeField(help_text="When the session is scheduled")
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Session duration in minutes")
    
    status = models.CharField(max_length=2, choices=SESSION_STATUS_CHOICES, default='P')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Session feedback (optional)
    teacher_rating = models.PositiveIntegerField(null=True, blank=True, help_text="Rating from teacher (1-5)")
    learner_rating = models.PositiveIntegerField(null=True, blank=True, help_text="Rating from learner (1-5)")
    teacher_feedback = models.TextField(max_length=500, blank=True, help_text="Feedback from teacher")
    learner_feedback = models.TextField(max_length=500, blank=True, help_text="Feedback from learner")

    def __str__(self):
        return f"{self.teacher.username} teaching {self.learner.username} - {self.skill.name}"

    @property
    def status_display(self):
        return dict(self.SESSION_STATUS_CHOICES)[self.status]

    @property
    def session_type_display(self):
        return dict(self.SESSION_TYPE_CHOICES)[self.session_type]

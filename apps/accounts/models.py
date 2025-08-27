from django.db import models
from django.contrib.auth.hashers import make_password
from apps.university.models import Department , Branch , University
import os 

def profile_images(instance,filename):
    return os.path.join('profile_images',instance.username,filename)

class User(models.Model):

    class Meta:
        ordering = ['-created_at']
        db_table = 'userprofile'

    YEAR_CHOICES = (
        ('1','First Year'),
        ('2','Second Year'),
        ('3','Third Year'),
        ('4','Fourth Year'),
    )
    GENDER_CHOICES = (
        ('M' , 'Male'),
        ('F' , 'Female'),
        ('O' , 'Other'),
    )
    username = models.CharField(max_length=25,unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    profile_pic = models.ImageField(upload_to=profile_images , blank=True , null=True)
    university_name = models.ForeignKey(University,on_delete=models.SET_NULL,null=True)
    personal_email = models.EmailField(unique=True,help_text="Use Your Personal Email Address")
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name='students')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,related_name='students')
    year = models.CharField(max_length=20,choices=YEAR_CHOICES)
    bio = models.TextField(max_length=250,blank=True,help_text="Tell Others About Yourself")
    current_password = models.CharField(max_length = 128)
    previous_password = models.CharField(max_length = 128,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self,raw_passoword):
        self.current_password = make_password(raw_passoword)

    def check_password(self,raw_password):
        from django.contrib.auth.handlers import check_password
        return check_password(raw_password,self.current_password)
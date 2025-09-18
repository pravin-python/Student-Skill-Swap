from rest_framework import serializers
from .models import Blog
from apps.accounts.models import User
from apps.category_skills.models import SkillsCategory

# Serializers for fetching the blogs using REST API

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username"]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillsCategory
        fields = ["id" , "name"]

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()

    class Meta:
        model = Blog
        fields = ["id" , "author" , "title" , "category" , "image" , "created_at"]

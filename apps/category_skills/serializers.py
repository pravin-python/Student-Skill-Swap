from rest_framework import serializers
from apps.accounts.models import User
from .models import SkillsCategory , Skills , UserSkills

# Serializers for displaying skills
class SkillsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsCategory
        fields = ["name"]

class UserBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name"]

class UserSkillSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()

    class Meta:
        model = UserSkills
        fields = ["user"]

class SkillSerializer(serializers.ModelSerializer):
    category = SkillsCategorySerializer()
    level_display = serializers.CharField(source="get_level_display")
    student = serializers.SerializerMethodField()

    class Meta:
        model = Skills
        fields = ["id", "name", "description",  "category" , "created_at" , "image" , "level_display" , "student"]
    
    def get_student(self, obj):
        user = self.context.get("user")
        return UserBasicSerializer(user).data if user else None


# Serializers for Displaying Instructors

class InstructorBasicSkillSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source="get_level_display")

    class Meta:
        model = Skills
        fields = ["name", "level_display"]

class InstructorBasicSerializer(serializers.ModelSerializer):

    department= serializers.CharField(source="department.name" , read_only=True)

    class Meta:
        model = User
        fields = ["id" , "first_name" , "last_name" , "profile_pic" , "bio" , "year" , "department"]

class InstructorSerializer(serializers.Serializer):
    user = InstructorBasicSerializer()
    skills = InstructorBasicSkillSerializer(many=True)
    skills_count = serializers.IntegerField()

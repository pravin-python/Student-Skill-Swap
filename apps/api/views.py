from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.accounts.models import User
from apps.category_skills.models import Skills, UserSkills
from apps.category_skills.serializers import SkillSerializer , InstructorSerializer
from apps.blog.serializers import BlogSerializer
from rest_framework.pagination import PageNumberPagination
from apps.blog.models import Blog
import random

# API to fetch the courses in HomePage
class HomeAPICoursesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.session.get("user_id")

        # Get all user_skills, optionally excluding current user
        user_skills_qs = UserSkills.objects.all()
        if user_id:
            user_skills_qs = user_skills_qs.exclude(user_id=user_id)

        # Get unique skill IDs
        skill_ids = list(user_skills_qs.values_list('skill_id', flat=True).distinct())
        random.shuffle(skill_ids)
        skill_ids = skill_ids[:6]

        # For each skill, pick a random user who has it
        skill_to_user = {}
        for skill_id in skill_ids:
            users_for_skill = list(user_skills_qs.filter(skill_id=skill_id).values_list('user_id', flat=True))
            skill_to_user[skill_id] = random.choice(users_for_skill)

        # Fetch actual Skills objects
        skills = Skills.objects.filter(id__in=skill_ids)

        # Serialize with random user context
        flattened_skills = []
        for skill in skills:
            user_for_context = User.objects.get(id=skill_to_user[skill.id])
            skill_data = SkillSerializer(skill, context={"user": user_for_context}).data
            flattened_skills.append(skill_data)

        return Response({"skills": flattened_skills})

# API to display the instructors in homepage
class HomeAPIInstructorView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.session.get("user_id")

        # Get all users who have added skills
        users_with_skills = User.objects.filter(user_skills__isnull=False).distinct().prefetch_related('user_skills__skill__category')

        if user_id:
            users_with_skills = users_with_skills.exclude(id=user_id)

        # Shuffle and pick 8 random instructors
        users_list = list(users_with_skills)
        random.shuffle(users_list)
        selected_users = users_list[:8]

        # Prepare instructor data
        instructors_data = []
        for user in selected_users:
            user_skills = [us.skill for us in user.user_skills.all()]
            instructors_data.append({
                'user': user,
                'skills': user_skills[:3],
                'skills_count': len(user_skills)
            })

        serializer = InstructorSerializer(instructors_data, many=True)
        return Response({"instructors_data": serializer.data})


# Custom pagination for infinite scroll
class InfiniteScrollPagination(PageNumberPagination):
    page_size = 6  # how many blogs to load per request
    page_size_query_param = "page_size"  # allow client to override ?page_size=10
    max_page_size = 50

# API View to fetch the blogs
class BlogAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        custom_user = request.session.get("user_id")
        blogs = Blog.objects.filter(is_published=True).select_related("author", "category").prefetch_related("images")
        
        if custom_user:
            blogs = blogs.exclude(author=custom_user)

        paginator = InfiniteScrollPagination()
        result_page = paginator.paginate_queryset(blogs, request, view=self)

        serializer = BlogSerializer(result_page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)



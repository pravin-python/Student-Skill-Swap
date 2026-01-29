from rest_framework import serializers
from .models import Blog , BlogImages
from apps.accounts.models import User
from apps.category_skills.models import SkillsCategory

# Serializers for fetching the blogs using REST API

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id" , "username"]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillsCategory
        fields = ["id" , "name"]


class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    thumbnail_image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ["id" , "author" , "title" , "category" , "thumbnail_image" , "created_at"]

    def get_thumbnail_image(self, obj):
        thumbnail_image = obj.images.filter(thumbnail=True).first()
        if thumbnail_image:
            request = self.context.get("request")
            return request.build_absolute_uri(thumbnail_image.image.url) if request else thumbnail_image.image.url
        return None
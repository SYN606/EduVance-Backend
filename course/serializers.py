from rest_framework import serializers
from .models import CourseCategory, Course


class CourseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'slug']


class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer()

    class Meta:
        model = Course
        fields = [
            'id', 'category', 'slug', 'description', 'duration', 'modules',
            'additional_details', 'main_image', 'additional_images'
        ]

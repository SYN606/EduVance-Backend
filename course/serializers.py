from rest_framework import serializers
from .models import CourseCategory, CourseDetails


class CourseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDetails
        fields = [
            'id', 'course_title', 'slug', 'main_image', 'additional_images',
            'description', 'modules', 'duration', 'highlights'
        ]


class CourseCategorySerializer(serializers.ModelSerializer):
    courses = CourseDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'slug',
                  'courses']  

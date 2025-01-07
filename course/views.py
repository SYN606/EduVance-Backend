from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import CourseCategorySerializer, CourseDetailsSerializer
from .models import CourseCategory, CourseDetails


class CourseCategoryListView(APIView):
    """
    View to list all categories with their respective courses
    """

    def get(self, request):
        categories = CourseCategory.objects.all()
        serializer = CourseCategorySerializer(categories, many=True)
        return Response(serializer.data)


class CourseCategoryDetailView(APIView):
    """
    View to list all courses under a specific category
    """

    def get(self, request, category_slug):
        category = get_object_or_404(CourseCategory, slug=category_slug)
        courses = CourseDetails.objects.filter(category=category)
        course_serializer = CourseDetailsSerializer(courses, many=True)

        # Return category details along with the serialized courses
        return Response({
            'category': CourseCategorySerializer(category).data,
            'courses': course_serializer.data
        })


class CourseDetailView(APIView):
    """
    View to get the full details of a specific course inside a category
    """

    def get(self, request, category_slug, course_slug):
        # Retrieve category and course
        category = get_object_or_404(CourseCategory, slug=category_slug)
        course = get_object_or_404(CourseDetails,
                                   slug=course_slug,
                                   category=category)

        # Serialize the course details
        course_serializer = CourseDetailsSerializer(course)

        return Response(course_serializer.data)

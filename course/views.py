# from django.shortcuts import render
from rest_framework import viewsets
from .models import Course, CourseCategory
from .serializers import CourseSerializer, CourseCategorySerializer


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

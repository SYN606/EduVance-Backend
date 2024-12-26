# course/urls.py

from django.urls import path
from .views import CourseCategoryListView, CourseCategoryDetailView, CourseDetailView

urlpatterns = [
    # List all categories with their courses
    path('api/courses/',
         CourseCategoryListView.as_view(),
         name='course-category-list'),

    # List courses under a specific category
    path('api/courses/<str:category_slug>/',
         CourseCategoryDetailView.as_view(),
         name='course-category-detail'),

    # Get full details of a specific course
    path('api/courses/<str:category_slug>/<str:course_slug>/',
         CourseDetailView.as_view(),
         name='course-detail'),
]

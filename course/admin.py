from django.contrib import admin
from .models import CourseCategory, CourseDetails


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    readonly_fields = ('slug',)


@admin.register(CourseDetails)
class CourseDetailsAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'category', 'slug', 'duration')
    readonly_fields = ('slug',)
    list_filter = ('category',)
    search_fields = ('course_title', 'category__name')

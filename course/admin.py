from django.contrib import admin
from .models import CourseCategory, Course
from django.utils.html import mark_safe


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    list_filter = ('name', )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug', 'description', 'duration',
                    'main_image_preview')

    def main_image_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.main_image.url}" width="100" height="100" />'
        ) if obj.main_image else "No image"

    main_image_preview.short_description = 'Main Image'

    search_fields = ('category__name', 'slug', 'description')
    list_filter = ('category', )
    prepopulated_fields = {'slug': ('description', )}
    ordering = ('category', )

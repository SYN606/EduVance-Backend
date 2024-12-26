from django.db import models
from django.utils.text import slugify


class CourseCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'


class Course(models.Model):
    category = models.ForeignKey(CourseCategory,
                                 on_delete=models.CASCADE,
                                 related_name='courses')

    course_title = models.CharField(max_length=255)  # Field for course title
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    modules = models.TextField()
    additional_details = models.TextField(blank=True, null=True)

    main_image = models.ImageField(upload_to='courses/',
                                   verbose_name="Main Image")
    additional_images = models.ImageField(
        upload_to='courses/additional/',
        blank=True,
        null=True,
        verbose_name="Additional Image",
        help_text="You can upload more images (optional)",
        max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.course_title)  # Generate slug from course title
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.course_title}"

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

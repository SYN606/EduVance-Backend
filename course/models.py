from django.db import models
from django.utils.text import slugify


class CourseCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Ensure unique slug
        original_slug = self.slug
        queryset = CourseCategory.objects.filter(slug=self.slug).exclude(
            pk=self.pk)
        counter = 1
        while queryset.exists():
            self.slug = f"{original_slug}-{counter}"
            queryset = CourseCategory.objects.filter(slug=self.slug).exclude(
                pk=self.pk)
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'


class CourseDetails(models.Model):
    category = models.ForeignKey(CourseCategory,
                                 on_delete=models.CASCADE,
                                 related_name='courses')
    course_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Will be auto-generated
    main_image = models.ImageField(upload_to='courses/',
                                   verbose_name="Main Image")
    additional_images = models.ImageField(
        upload_to='courses/additional/',
        blank=True,
        null=True,
        verbose_name="Additional Image",
        help_text="You can upload more images (optional)",
        max_length=200)
    description = models.TextField()
    modules = models.TextField()
    duration = models.CharField(max_length=100)
    highlights = models.TextField(blank=True,
                                  null=True,
                                  help_text="Course highlights (optional)")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.slug}/{self.course_title}")

        original_slug = self.slug
        queryset = CourseDetails.objects.filter(slug=self.slug).exclude(
            pk=self.pk)
        counter = 1
        while queryset.exists():
            self.slug = f"{original_slug}-{counter}"
            queryset = CourseDetails.objects.filter(slug=self.slug).exclude(
                pk=self.pk)
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.course_title}"

    class Meta:
        verbose_name = 'Course Detail'
        verbose_name_plural = 'Course Details'

from django.db import models
from django.utils.text import slugify


class CourseCategory(models.Model):
    COMPUTER_BASICS = 'CB'
    WEB_DEVELOPMENT = 'WD'
    CYBER_SECURITY = 'CS'
    MECHANICAL_CIVIL_ENGINEERING = 'MCE'

    CATEGORY_CHOICES = [
        (COMPUTER_BASICS, 'Computer Basics'),
        (WEB_DEVELOPMENT, 'Web Development'),
        (CYBER_SECURITY, 'Cyber Security'),
        (MECHANICAL_CIVIL_ENGINEERING, 'Mechanical and Civil Engineering'),
    ]

    name = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default=COMPUTER_BASICS,
    )
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.get_name_display())  # Slug from the display name
        super().save(*args, **kwargs)

    def __str__(self):
        return dict(self.CATEGORY_CHOICES).get(self.name, self.name)

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'


class Course(models.Model):
    category = models.ForeignKey(CourseCategory,
                                 on_delete=models.CASCADE,
                                 related_name='courses')

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
            self.slug = slugify(self.description[:50])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.slug}"

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

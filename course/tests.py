from django.test import TestCase
from .models import CourseCategory, Course
from django.core.exceptions import ValidationError


class CourseCategoryModelTest(TestCase):

    def test_create_course_category(self):
        category = CourseCategory.objects.create(name='Computer Basics')
        self.assertEqual(category.name, 'Computer Basics')
        self.assertEqual(CourseCategory.objects.count(), 1)

    def test_category_slug_generation(self):
        category = CourseCategory.objects.create(name='Web Development')
        self.assertEqual(category.slug, 'web-development')


class CourseModelTest(TestCase):

    def setUp(self):
        category = CourseCategory.objects.create(name='Cyber Security')
        self.course_data = {
            'category': category,
            'description': 'Introduction to Cyber Security',
            'duration': '6 months',
            'modules': 'Module 1: Basics, Module 2: Security',
            'main_image':
            'path/to/main_image.jpg',  # This should be a valid image path
        }

    def test_create_course(self):
        category = CourseCategory.objects.get(name='Cyber Security')
        course = Course.objects.create(**self.course_data)

        self.assertEqual(course.category, category)
        self.assertEqual(course.description, 'Introduction to Cyber Security')
        self.assertEqual(course.duration, '6 months')
        self.assertEqual(course.modules,
                         'Module 1: Basics, Module 2: Security')

    def test_course_slug_generation(self):
        category = CourseCategory.objects.get(name='Cyber Security')
        course = Course.objects.create(
            category=category,
            description='Advanced Cyber Security',
            duration='3 months',
            modules='Module 1: Advanced, Module 2: Encryption',
            main_image='path/to/main_image.jpg')
        self.assertEqual(course.slug, 'advanced-cyber-security')

    def test_course_category_relation(self):
        category = CourseCategory.objects.create(
            name='Mechanical and Civil Engineering')
        course = Course.objects.create(
            category=category,
            description='Introduction to Civil Engineering',
            duration='1 year',
            modules='Module 1: Basics, Module 2: Structural Engineering',
            main_image='path/to/main_image.jpg')
        self.assertEqual(course.category.name,
                         'Mechanical and Civil Engineering')

    def test_course_with_missing_image(self):
        category = CourseCategory.objects.create(name='Web Development')
        course = Course(
            category=category,
            description='Full-stack Web Development',
            duration='6 months',
            modules='Module 1: Frontend, Module 2: Backend',
            main_image=None  # Missing image
        )
        with self.assertRaises(ValidationError):
            course.full_clean(
            )  # Should raise a validation error because the image is mandatory

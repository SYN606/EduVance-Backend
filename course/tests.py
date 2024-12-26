from django.test import TestCase
from .models import CourseCategory, CourseDetails


class CourseSlugTestCase(TestCase):

    def setUp(self):
        # Create a category and course for testing
        self.category = CourseCategory.objects.create(name="Cyber Security",
                                                      slug="cyber-security")
        self.course = CourseDetails.objects.create(
            category=self.category,
            course_title="Ethical Hacking",
            main_image="path/to/image",
            description="Description of Ethical Hacking",
            modules="Module 1, Module 2",
            duration="6 months")

    def test_unique_course_slug(self):
        # Create a duplicate course to check for unique slug generation
        duplicate_course = CourseDetails.objects.create(
            category=self.category,
            course_title="Ethical Hacking",
            main_image="path/to/image",
            description="Description of Ethical Hacking",
            modules="Module 1, Module 2",
            duration="6 months")
        
        self.assertTrue(
            duplicate_course.slug.startswith("cyber-security/ethical-hacking"))
        self.assertNotEqual(self.course.slug, duplicate_course.slug)

# Generated by Django 5.1.4 on 2024-12-26 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_course_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('main_image', models.ImageField(upload_to='courses/', verbose_name='Main Image')),
                ('additional_images', models.ImageField(blank=True, help_text='You can upload more images (optional)', max_length=200, null=True, upload_to='courses/additional/', verbose_name='Additional Image')),
                ('description', models.TextField()),
                ('modules', models.TextField()),
                ('duration', models.CharField(max_length=100)),
                ('highlights', models.TextField(blank=True, help_text='Course highlights (optional)', null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='course.coursecategory')),
            ],
            options={
                'verbose_name': 'Course Detail',
                'verbose_name_plural': 'Course Details',
            },
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]

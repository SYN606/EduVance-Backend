# Generated by Django 5.1.4 on 2025-01-08 07:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=100, unique=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='student_profiles/')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('college_or_school', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('enrolled_course_duration', models.CharField(max_length=255)),
                ('fees_left', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

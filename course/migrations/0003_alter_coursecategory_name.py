# Generated by Django 5.1.4 on 2024-12-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_coursecategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecategory',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]

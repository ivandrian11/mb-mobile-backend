# Generated by Django 4.1.1 on 2022-10-12 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0002_course_project_material_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='complete',
        ),
    ]

# Generated by Django 4.1.1 on 2022-10-24 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0010_rename_project_ins_course_project_instruction'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.1.1 on 2022-10-23 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0008_certificate_user_project_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='question',
            new_name='feedback',
        ),
        migrations.AddField(
            model_name='course',
            name='project_ins',
            field=models.TextField(null=True),
        ),
    ]
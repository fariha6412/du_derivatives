# Generated by Django 4.1.7 on 2023-05-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_project_demo_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='deployed_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='github_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]

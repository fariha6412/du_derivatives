# Generated by Django 4.1.7 on 2023-05-04 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_project_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-rate',)},
        ),
    ]

# Generated by Django 2.2.3 on 2020-04-02 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20200401_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='Mechanical_Release_Scheduled',
            new_name='MilestoneOne_Scheduled',
        ),
    ]

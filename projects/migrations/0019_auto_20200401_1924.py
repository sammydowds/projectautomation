# Generated by Django 2.2.3 on 2020-04-02 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20200401_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='initialproject',
            old_name='Milestone_1',
            new_name='MilestoneOne',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Milestone_1',
            new_name='MilestoneOne',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Milestone_1_Complete',
            new_name='MilestoneOne_Complete',
        ),
    ]
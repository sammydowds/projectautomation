# Generated by Django 2.1.4 on 2019-06-16 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='offtrack',
        ),
        migrations.RemoveField(
            model_name='project',
            name='onwatch',
        ),
        migrations.AddField(
            model_name='project',
            name='Status',
            field=models.CharField(choices=[('OT', 'Off Track'), ('OW', 'On Watch'), ('OH', 'On Hold'), ('U', 'Update')], default='OT', max_length=1),
        ),
    ]

# Generated by Django 2.1.4 on 2019-01-29 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_pastprojects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pastprojects',
            name='employees',
        ),
        migrations.AddField(
            model_name='project',
            name='iscurrent',
            field=models.BooleanField(null=True),
        ),
        migrations.DeleteModel(
            name='PastProjects',
        ),
    ]

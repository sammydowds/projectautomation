# Generated by Django 2.2.3 on 2019-07-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='Summary',
            field=models.CharField(default='Enter Project Comments.', max_length=50, null=True),
        ),
    ]

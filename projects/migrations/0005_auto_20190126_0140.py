# Generated by Django 2.1.4 on 2019-01-26 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20190124_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='projectname',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 2.1.4 on 2019-07-10 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20190705_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='projectname',
            field=models.CharField(max_length=50),
        ),
    ]

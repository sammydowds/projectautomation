# Generated by Django 2.2.3 on 2019-11-03 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20191103_1224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='Install_Scheduled',
            new_name='Install_Finish_Scheduled',
        ),
        migrations.AddField(
            model_name='project',
            name='Install_Start_Scheduled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Finishing_Scheduled',
            field=models.BooleanField(default=True),
        ),
    ]
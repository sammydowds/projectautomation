# Generated by Django 2.2.3 on 2019-09-21 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20190919_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='Assembly_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Customer_Runoff_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Documentation_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Electrical_Release_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Finishing_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Install_Finish_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Install_Start_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Internal_Runoff_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Manufacturing_Complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='Ship_Complete',
            field=models.BooleanField(default=False),
        ),
    ]
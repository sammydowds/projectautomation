# Generated by Django 2.1.4 on 2019-01-20 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20190120_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assembly',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='customerrunoff',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='documentation',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='electricalrelease',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='finishing',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='installfinish',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='installstart',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='integration',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='internalrunoff',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='manufacturing',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='ship',
            field=models.DateField(null=True),
        ),
    ]

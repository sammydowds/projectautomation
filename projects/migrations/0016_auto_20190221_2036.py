# Generated by Django 2.1.4 on 2019-02-22 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20190221_2034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='customer_runoff',
            new_name='customerrunoff',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='electrical_release',
            new_name='electricalrelease',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='install_finish',
            new_name='installfinish',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='install_start',
            new_name='installstart',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='internal_runoff',
            new_name='internalrunoff',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='mechanical_release',
            new_name='mechanicalrelease',
        ),
    ]

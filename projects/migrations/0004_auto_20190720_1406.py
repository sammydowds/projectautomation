# Generated by Django 2.2.3 on 2019-07-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20190720_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='Summary',
            field=models.CharField(default='Enter Project Comments.', max_length=255, null=True),
        ),
    ]
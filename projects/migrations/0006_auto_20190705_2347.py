# Generated by Django 2.1.4 on 2019-07-05 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20190702_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialproject',
            name='projectnumber',
            field=models.IntegerField(),
        ),
    ]
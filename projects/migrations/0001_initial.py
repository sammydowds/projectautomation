# Generated by Django 2.1.4 on 2019-01-20 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectnumber', models.IntegerField()),
                ('projectname', models.CharField(max_length=30)),
                ('mechanicalrelease', models.DateField()),
                ('electricalrelease', models.DateField()),
                ('manufacturing', models.DateField()),
                ('finishing', models.DateField()),
                ('assembly', models.DateField()),
                ('integration', models.DateField()),
                ('internalrunoff', models.DateField()),
                ('customerrunoff', models.DateField()),
                ('ship', models.DateField()),
                ('installstart', models.DateField()),
                ('installfinish', models.DateField()),
                ('documentation', models.DateField()),
                ('employees', models.ManyToManyField(to='projects.Employee')),
            ],
        ),
    ]

# Generated by Django 2.2.3 on 2020-04-02 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20200401_1934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='Assembly_Complete',
            new_name='MilestoneFive_Complete',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Assembly_Scheduled',
            new_name='MilestoneFive_Scheduled',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Customer_Runoff_Complete',
            new_name='MilestoneFour_Complete',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Customer_Runoff_Scheduled',
            new_name='MilestoneFour_Scheduled',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Documentation_Complete',
            new_name='MilestoneSeven_Complete',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Documentation_Scheduled',
            new_name='MilestoneSeven_Scheduled',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Electrical_Release_Complete',
            new_name='MilestoneSix_Complete',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Electrical_Release_Scheduled',
            new_name='MilestoneSix_Scheduled',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Finishing_Complete',
            new_name='MilestoneThree_Complete',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Install_Finish_Complete',
            new_name='MilestoneThree_Scheduled',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Install_Finish_Scheduled',
            new_name='MilestoneTwo_Complete',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='Install_Start_Complete',
            new_name='MilestoneTwo_Scheduled',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Assembly',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Customer_Runoff',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Documentation',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Electrical_Release',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Finishing',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Finishing_Scheduled',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Install_Finish',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Install_Start',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Install_Start_Scheduled',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Internal_Runoff',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Internal_Runoff_Complete',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Internal_Runoff_Scheduled',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Manufacturing',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Manufacturing_Complete',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Manufacturing_Scheduled',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Ship',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Ship_Complete',
        ),
        migrations.RemoveField(
            model_name='project',
            name='Ship_Scheduled',
        ),
        migrations.AddField(
            model_name='project',
            name='MilestoneFive',
            field=models.DateField(blank=True, null=True, verbose_name='Milestone 5'),
        ),
        migrations.AddField(
            model_name='project',
            name='MilestoneFour',
            field=models.DateField(blank=True, null=True, verbose_name='Milestone 4'),
        ),
        migrations.AddField(
            model_name='project',
            name='MilestoneSeven',
            field=models.DateField(blank=True, null=True, verbose_name='Milestone 7'),
        ),
        migrations.AddField(
            model_name='project',
            name='MilestoneSix',
            field=models.DateField(blank=True, null=True, verbose_name='Milestone 6'),
        ),
        migrations.AddField(
            model_name='project',
            name='MilestoneThree',
            field=models.DateField(blank=True, null=True, verbose_name='Milestone 3'),
        ),
        migrations.AddField(
            model_name='project',
            name='MilestoneTwo',
            field=models.DateField(blank=True, null=True, verbose_name='Milestone 2'),
        ),
    ]

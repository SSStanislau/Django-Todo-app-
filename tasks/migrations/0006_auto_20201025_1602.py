# Generated by Django 3.1.2 on 2020-10-25 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20201025_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='execution_day',
            new_name='day_of_status_change',
        ),
    ]
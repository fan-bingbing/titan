# Generated by Django 2.2.4 on 2019-10-21 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0025_auto_20191021_1332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acsout',
            old_name='TimeStamp',
            new_name='timeStamp',
        ),
    ]

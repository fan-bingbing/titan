# Generated by Django 2.2.4 on 2019-10-02 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0013_auto_20191002_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='madout',
            old_name='audiofreqz_Hz',
            new_name='audiofreq_Hz',
        ),
    ]
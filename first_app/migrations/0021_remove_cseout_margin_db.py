# Generated by Django 2.2.4 on 2019-10-03 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0020_auto_20191003_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cseout',
            name='margin_dB',
        ),
    ]

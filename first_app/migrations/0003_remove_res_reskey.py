# Generated by Django 2.2.4 on 2019-09-27 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_res'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='res',
            name='reskey',
        ),
    ]
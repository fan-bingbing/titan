# Generated by Django 2.2.4 on 2019-11-04 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0054_auto_20191104_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acpout',
            name='id',
        ),
        migrations.AddField(
            model_name='acpout',
            name='Test_name',
            field=models.CharField(default='', max_length=200, primary_key=True, serialize=False),
        ),
    ]

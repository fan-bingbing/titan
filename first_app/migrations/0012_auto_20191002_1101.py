# Generated by Django 2.2.4 on 2019-10-02 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0011_auto_20191001_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='madout',
            name='id',
        ),
        migrations.AlterField(
            model_name='madout',
            name='audiofreq',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
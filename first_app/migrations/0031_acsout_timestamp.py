# Generated by Django 2.2.4 on 2019-10-21 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0030_auto_20191021_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='acsout',
            name='TimeStamp',
            field=models.CharField(default='null', max_length=200),
            preserve_default=False,
        ),
    ]

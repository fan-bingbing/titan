# Generated by Django 2.2.4 on 2019-10-30 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0035_auto_20191030_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='blkout',
            name='Test_number',
            field=models.CharField(default='', max_length=200),
        ),
    ]

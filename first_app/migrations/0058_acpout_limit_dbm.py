# Generated by Django 2.2.4 on 2019-11-04 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0057_auto_20191104_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='acpout',
            name='limit_dBm',
            field=models.CharField(default='', max_length=200),
        ),
    ]
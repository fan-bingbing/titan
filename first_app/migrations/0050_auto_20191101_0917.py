# Generated by Django 2.2.4 on 2019-10-31 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0049_auto_20191101_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='madout',
            name='Test_name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]

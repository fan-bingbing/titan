# Generated by Django 2.2.4 on 2019-10-30 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0043_auto_20191031_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acsout',
            name='id',
        ),
        migrations.AlterField(
            model_name='acsout',
            name='Test_name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]

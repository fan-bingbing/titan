# Generated by Django 2.2.4 on 2019-10-31 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0047_auto_20191031_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='srout',
            name='Test_name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]

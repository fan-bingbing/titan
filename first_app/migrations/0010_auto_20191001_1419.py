# Generated by Django 2.2.4 on 2019-10-01 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0009_madout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='madout',
            name='audiofreq',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='madout',
            name='audiolev',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='madout',
            name='avepeak',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='madout',
            name='limit',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='madout',
            name='margin',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='madout',
            name='minuspeak',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='madout',
            name='pluspeak',
            field=models.FloatField(max_length=200),
        ),
    ]

# Generated by Django 2.2.4 on 2019-10-01 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0008_txsig'),
    ]

    operations = [
        migrations.CreateModel(
            name='MADOUT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audiofreq', models.CharField(max_length=200)),
                ('audiolev', models.CharField(max_length=200)),
                ('pluspeak', models.CharField(max_length=200)),
                ('minuspeak', models.CharField(max_length=200)),
                ('avepeak', models.CharField(max_length=200)),
                ('limit', models.CharField(max_length=200)),
                ('margin', models.CharField(max_length=200)),
                ('timestamp', models.CharField(max_length=200)),
            ],
        ),
    ]

# Generated by Django 2.2.4 on 2019-10-27 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0032_auto_20191021_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='BLKOUT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CH_Freq_MHz', models.CharField(max_length=200)),
                ('CH_Lev_dBuV', models.CharField(max_length=200)),
                ('IN_Freq_MHz', models.FloatField(max_length=200)),
                ('IN_Lev_dBuV', models.CharField(max_length=200)),
                ('BLK_dB', models.FloatField(max_length=200)),
                ('limit_dB', models.FloatField(max_length=200)),
                ('TimeStamp', models.CharField(max_length=200)),
            ],
        ),
    ]

# Generated by Django 2.2.4 on 2019-10-03 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0019_cseout'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cseout',
            old_name='limit_kHz',
            new_name='limit_dBm',
        ),
        migrations.RenameField(
            model_name='cseout',
            old_name='margin_kHz',
            new_name='margin_dB',
        ),
    ]
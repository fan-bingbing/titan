# Generated by Django 2.2.4 on 2019-11-04 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0067_cshout'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fepout',
            old_name='Freq_Error_MHz',
            new_name='Freq_Error_Hz',
        ),
        migrations.RenameField(
            model_name='fepout',
            old_name='Power_dBm',
            new_name='Power_diff_dB',
        ),
        migrations.RenameField(
            model_name='fepout',
            old_name='Power_limit_dBm',
            new_name='Power_diff_limit_dB',
        ),
    ]
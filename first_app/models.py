from django.db import models

# Create your models here.
class FEP(models.Model):
    parameter = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter

class ACP(models.Model):
    parameter = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter

class CSE(models.Model):
    parameter = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter

class FEPOUT(models.Model):
    Test_name = models.CharField(primary_key=True, max_length=200)
    CH_Freq_MHz = models.CharField(max_length=200)
    Freq_Error_MHz = models.FloatField(max_length=200)
    Fre_error_limit_Hz = models.FloatField(max_length=200)
    Power_dBm = models.FloatField(max_length=200)
    Power_limit_dBm = models.FloatField(max_length=200)
    Screenshot_file = models.CharField(max_length=200)
    TimeStamp = models.CharField(max_length=200)

    def __str__(self):
        return self.Test_name

class CSEOUT(models.Model):
    SubRange = models.CharField(max_length=200)
    CSE1_Frequency_MHz = models.FloatField(max_length=200)
    CSE1_Level_dBm = models.FloatField(max_length=200)
    CSE2_Frequency_MHz = models.FloatField(max_length=200)
    CSE2_Level_dBm = models.FloatField(max_length=200)
    limit_dBm = models.FloatField(max_length=200)
    Screenshot_file = models.CharField(max_length=200)
    def __str__(self):
        return self.SubRange

class CSHOUT(models.Model):
    SubRange = models.CharField(max_length=200)
    CSE1_Frequency_MHz = models.FloatField(max_length=200)
    CSE1_Level_dBm = models.FloatField(max_length=200)
    CSE2_Frequency_MHz = models.FloatField(max_length=200)
    CSE2_Level_dBm = models.FloatField(max_length=200)
    limit_dBm = models.FloatField(max_length=200)
    Screenshot_file = models.CharField(max_length=200)


    def __str__(self):
        return self.SubRange

class ACPOUT(models.Model):
    Test_name = models.CharField(primary_key=True, max_length=200)
    Frequency_MHz = models.CharField(max_length=200)
    CarrierPower_dBm = models.FloatField(max_length=200)
    ACPminus_dBc = models.FloatField(max_length=200)
    ACPplus_dBc = models.FloatField(max_length=200)
    limit_dBm = models.FloatField(max_length=200)
    Screenshot_file = models.CharField(max_length=200)
    TimeStamp = models.CharField(max_length=200)


    def __str__(self):
        return self.Test_name


class RES(models.Model):

    resadd = models.CharField(max_length=200)
    resid = models.CharField(max_length=200)

    def __str__(self):
        return self.resadd

class DEMOD(models.Model):
    parameter = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter

class TXSIG(models.Model):
    parameter = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter

class RXSIG(models.Model):
    parameter = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter

class ACSOUT(models.Model):
    Test_name = models.CharField(primary_key=True, max_length=200)
    CH_Freq_MHz = models.CharField(max_length=200)
    CH_Lev_dBuV = models.FloatField(max_length=200)
    IN_Freq_MHz = models.FloatField(max_length=200)
    IN_Lev_dBuV = models.FloatField(max_length=200)
    ACS_dB = models.FloatField(max_length=200)
    limit_dB = models.FloatField(max_length=200)
    TimeStamp = models.CharField(max_length=200)

    def __str__(self):
        return self.Test_name

class BLKOUT(models.Model):
    Test_name = models.CharField(primary_key=True, max_length=200)
    CH_Freq_MHz = models.CharField(max_length=200)
    CH_Lev_dBuV = models.FloatField(max_length=200)
    IN_Freq_MHz = models.FloatField(max_length=200)
    IN_Lev_dBuV = models.FloatField(max_length=200)
    BLK_dB = models.FloatField(max_length=200)
    limit_dB = models.FloatField(max_length=200)
    TimeStamp = models.CharField(max_length=200)

    def __str__(self):
        return self.Test_name

class SROUT(models.Model):
    Test_name = models.CharField(primary_key=True, max_length=200)
    CH_Freq_MHz = models.CharField(max_length=200)
    CH_Lev_dBuV = models.FloatField(max_length=200)
    IN_Freq_MHz = models.FloatField(max_length=200)
    IN_Lev_dBuV = models.FloatField(max_length=200)
    SR_dB = models.FloatField(max_length=200)
    limit_dB = models.FloatField(max_length=200)
    TimeStamp = models.CharField(max_length=200)

    def __str__(self):
        return self.Test_name


class MADOUT(models.Model):
    Test_name = models.CharField(primary_key=True, max_length=200)
    audiofreq_Hz = models.CharField(max_length=200)
    audiolev_mV = models.FloatField(max_length=200)
    pluspeak_kHz = models.FloatField(max_length=200)
    minuspeak_kHz = models.FloatField(max_length=200)
    avepeak_kHz = models.FloatField(max_length=200)
    limit_kHz = models.FloatField(max_length=200)
    margin_kHz = models.FloatField(max_length=200)
    TimeStamp = models.CharField(max_length=200)

    def __str__(self):
        return self.audiofreq_Hz

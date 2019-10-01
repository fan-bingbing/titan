from django.db import models

# Create your models here.
class FEP(models.Model):
    parameter = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.parameter


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

class MADOUT(models.Model):

    audiofreq = models.CharField(max_length=200)
    audiolev = models.FloatField(max_length=200)
    pluspeak = models.FloatField(max_length=200)
    minuspeak = models.FloatField(max_length=200)
    avepeak = models.FloatField(max_length=200)
    limit = models.FloatField(max_length=200)
    margin = models.FloatField(max_length=200)
    timestamp = models.CharField(max_length=200)

    def __str__(self):
        return self.audiofreq

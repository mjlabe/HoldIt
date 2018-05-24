from django.db import models


class DModel(models.Model):
    fval = models.ForeignKey('HoldApp.DModelF', on_delete=models.CASCADE)
    dval = models.ForeignKey('HoldApp.DModelD', on_delete=models.CASCADE)


class DModelF(models.Model):
    fval = models.FloatField(max_length=100)


class DModelD(models.Model):
    dval = models.IntegerField()

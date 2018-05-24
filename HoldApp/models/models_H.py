from django.db import models


class HModelData(models.Model):
    data1 = models.CharField(max_length=100)
    data2 = models.CharField(max_length=100)
    data3 = models.CharField(max_length=100)


class HModelStuff(models.Model):
    stuff1 = models.CharField(max_length=100)
    stuff2 = models.CharField(max_length=100)
    stuff3 = models.CharField(max_length=100)


class HModel(models.Model):
    data = models.ForeignKey(HModelData, on_delete=models.CASCADE)
    stuff = models.ForeignKey(HModelStuff, on_delete=models.CASCADE)

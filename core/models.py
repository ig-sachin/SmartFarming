from django.db import models

# Create your models here.

class Blog(models.Model):
    bid = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=500)
    category=models.CharField(max_length=500)
    date=models.DateField()
    description=models.TextField()
    process=models.TextField()
    uses=models.TextField()
    others=models.CharField(max_length=3000)
    conclusion=models.CharField(max_length=1000)
    images=models.ImageField(upload_to='blogs/image/')

class CropInfo(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()

class FertilizerInfo(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()


class PreviousCropPred(models.Model):
    nitrogen = models.IntegerField()
    phosphorous = models.IntegerField()
    potassium = models.IntegerField()
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    ph = models.IntegerField()
    rain = models.IntegerField()
    crop = models.CharField(max_length=100)

class PreviousFertilizerPred(models.Model):
    nitrogen = models.IntegerField()
    phosphorous = models.IntegerField()
    potassium = models.IntegerField()
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    moisture = models.IntegerField()
    soil = models.CharField(max_length=100)
    crop = models.CharField(max_length=100)
    fertilizer=models.CharField(max_length=100)

class CropState(models.Model):
    stateName = models.CharField(max_length=200)
    districtName = models.CharField(max_length=200)
    cropYear = models.IntegerField()
    season = models.CharField(max_length=200)
    crop = models.CharField(max_length=200)
    area = models.FloatField()
    production = models.FloatField()
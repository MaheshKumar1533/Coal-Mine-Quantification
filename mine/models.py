from django.db import models
from django.contrib.auth.models import AbstractUser


class mineDetail(AbstractUser):
    type_choices = [
        ('UnderGround', 'UnderGround'),
        ('OpenCast', 'OpenCast'),]
    coal_type = models.CharField(max_length=50,choices=type_choices,default='UnderGround')
    latitude = models.FloatField()
    longitude = models.FloatField()
    area = models.FloatField(default=0)
    green_area = models.FloatField(default=0)
    mine_area = models.FloatField(default=0)
    bare_land = models.BooleanField(default=0)

class fueltype(models.Model):
    username = models.ForeignKey(mineDetail, on_delete=models.CASCADE)
    fuel_choice = [
        ('Diesel', 'Diesel'),
        ('Gasoline', 'Gasoline'),
        ('naturalGas', 'NaturalGas'),
    ]
    transport = models.CharField(max_length=30,choices=fuel_choice,default='Diesel')
    toolUsage = models.CharField(max_length=30,choices=fuel_choice,default='Diesel')
    
class explosion(models.Model):
    username = models.ForeignKey(mineDetail, on_delete=models.CASCADE)
    explosiveType = models.CharField(max_length=30)
    emissionFactor = models.FloatField()
    
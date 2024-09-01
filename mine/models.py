from django.db import models
from django.contrib.auth.models import AbstractUser


class mineDetail(AbstractUser):
    type_choices = [
        ('UnderGround', 'UnderGround'),
        ('OpenCast', 'OpenCast'),]
    coal_type = models.CharField(max_length=50,choices=type_choices,default='UnderGround',null=True)
    area = models.FloatField(default=0,null=True)
    green_area = models.FloatField(default=0,null=True)
    mine_area = models.FloatField(default=0,null=True)
    bare_land = models.BooleanField(default=0,null=True)

class mineaddress(models.Model):
    username = models.ForeignKey(mineDetail, on_delete=models.CASCADE,related_name="address")
    street_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zip_code = models.IntegerField(null=True)
    country = models.CharField(max_length=50, null=True,default='India')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

class fueltype(models.Model):
    username = models.ForeignKey(mineDetail, on_delete=models.CASCADE)
    fuel_choice = [
        ('Diesel', 'Diesel'),
        ('Gasoline', 'Gasoline'),
        ('naturalGas', 'NaturalGas'),
    ]
    transport = models.CharField(max_length=30,choices=fuel_choice,default='Diesel',null=True)
    toolUsage = models.CharField(max_length=30,choices=fuel_choice,default='Diesel',null=True)
    
class explosion(models.Model):
    username = models.ForeignKey(mineDetail, on_delete=models.CASCADE,related_name="explos")
    explosiveType = models.CharField(max_length=30,null=True)
    emissionFactor = models.FloatField(null=True)
    
class emissions(models.Model):
    mine = models.ForeignKey(mineDetail, on_delete=models.CASCADE,related_name="emissions")
    total_emissions = models.FloatField(default=0)
    extraction_emissions = models.FloatField(default=0)
    transport_emissions = models.FloatField(default=0)
    pros_emissions = models.FloatField(default=0)
    tool_emissions = models.FloatField(default=0)
    def __str__(self):
        return f'{self.total_emissions}'
from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Building_Details(models.Model):
    Serial_Number=models.AutoField(primary_key=True)
    Building_UID=models.UUIDField(null=True)
    Name_of_Building=models.CharField(max_length=100)
    Location=models.CharField(max_length=100)
    Building_Number = models.IntegerField(null=True)
    GeometricLocation = models.GeometryField(spatial_index=True,null=True)
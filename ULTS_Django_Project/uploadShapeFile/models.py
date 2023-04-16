from django.db import models


# Create your models here.
class Building_Details(models.Model):
    Serial_NUmber=models.AutoField(primary_key=True)
    Name_of_Building=models.CharField(max_length=100)
    Location=models.CharField(max_length=100)
from django.db import models

# Create your models here.
class TopDisasters(models.Model):
    s_number = models.IntegerField()
    cityName = models.CharField(max_length=100)
    rainFall = models.CharField(max_length=100 ,default='0')
    temperature = models.CharField(max_length=100,default='0')
    humidity = models.DecimalField(max_digits=5, decimal_places=2,default = 0)
    windSpeed = models.DecimalField(max_digits=5, decimal_places=2,default = 0)

    def __str__(self):
        return self.cityName
    
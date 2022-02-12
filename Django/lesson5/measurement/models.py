from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class Measurment(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    temp = models.IntegerField()
    date = models.DateField(auto_now_add=True)
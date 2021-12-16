from django.db import models


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField()

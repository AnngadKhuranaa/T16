

# Create your models here.
from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.name


from datetime import datetime

from django.db import models
from django.db.models import CASCADE


class City(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=128)
    city = models.ForeignKey(City, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=128)
    street = models.ForeignKey(Street, on_delete=CASCADE)
    house = models.CharField(max_length=128)
    close_time = models.TimeField()
    open_time = models.TimeField()
    city = models.ForeignKey(City, on_delete=CASCADE)

    def open(self):
        if self.open_time < datetime.now().time() < self.close_time:
            return 1
        return 0

    def __str__(self):
        return self.name

from django.db import models
from authentication.models import User


class Trip(models.Model):
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    polyline = models.TextField()

    class Meta:
        ordering: ['-start_date']

    def __str__(self):
        return self.name


class Location(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    longitude = models.FloatField()
    latitude = models.FloatField()


class DayPlace(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    desc = models.TextField()

from django.db import models
from authentication.models import User


class Trip(models.Model):
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    polyline = models.TextField(blank=True)
    cover_url = models.CharField(max_length=255, null=True)

    class Meta:
        ordering: ['-start_date']

    def __str__(self):
        return self.name


class Location(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=250)
    place_id = models.TextField()


class DayPlace(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=250)
    visited = models.BooleanField()
    sort_id = models.IntegerField()


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    desc = models.TextField()

from django.contrib import admin
from trips.models import Trip, Post, Location, DayPlace

admin.site.register(Trip)
admin.site.register(Post)
admin.site.register(Location)
admin.site.register(DayPlace)

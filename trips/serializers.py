from rest_framework import serializers
from .models import Trip, Location, DayPlace


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ['id', 'name', 'start_date', 'polyline', 'created_by', 'cover_url']
        read_only_fields = ['created_by']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'place_id', 'trip']
        read_only_fields = ['trip']


class DayPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlace
        fields = ['id', 'name', 'location', 'sort_id', 'visited']
        read_only_fields = ['location']


class ImportSerializer(serializers.Serializer):
    file = serializers.FileField()



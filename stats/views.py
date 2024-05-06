from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView, Response, status
import datetime
from trips.models import Trip, Location, DayPlace


class TripSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, tid):
        trip = Trip.objects.get(id=tid)

        locations = Location.objects.filter(trip=trip)
        loc_val = locations.values()
        resp = []
        for loc in loc_val:
            place_num = DayPlace.objects.filter(location_id=loc['id']).count()
            resp.append({'group': loc['name'], 'value': place_num})

        return Response({'data': resp}, status=status.HTTP_200_OK)


class AllTripsSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        resp = []
        trips = Trip.objects.filter(created_by=request.user)

        for trip in trips:
            locations = Location.objects.filter(trip=trip)
            loc_val = locations.values()
            place_num = 0
            location_num = locations.count()
            for loc in loc_val:
                pln = DayPlace.objects.filter(location_id=loc['id']).count()
                place_num += pln
            resp.append({'group': 'Locations', 'date': trip.start_date, 'value': location_num})
            resp.append({'group': 'Places', 'date': trip.start_date, 'value': place_num})

        return Response({'data': resp}, status=status.HTTP_200_OK)


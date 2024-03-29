from django.shortcuts import render
from rest_framework.views import APIView, Response, status
import datetime
from trips.models import Trip


class TripSummaryStats(APIView):

    @staticmethod
    def get_creator(trip: Trip):
        return trip.created_by

    def get(self, request):
        today_date = datetime.date.today()
        year_ago = today_date - datetime.timedelta(days=365)
        trips = Trip.objects.filter(created_by=request.user, start_date__gte=year_ago, start_date__lte=today_date)

        final = {}
        creators = list(set(map(self.get_creator, trips)))

        for trip in trips:
            for creator in creators:
                final[trip] = creator

        return Response({'data': final}, status=status.HTTP_200_OK)

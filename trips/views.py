import json
from io import BytesIO

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from pandas import ExcelWriter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TripSerializer, LocationSerializer, DayPlaceSerializer, ImportSerializer
from .models import Trip, Location, DayPlace
from rest_framework import permissions, status
from .permissions import IsOwner, IsOwnerLocation, IsOwnerPlace
from .renderers import TripRenderer
import requests
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


# Trip
class TripListAPIView(ListCreateAPIView):
    renderer_classes = (TripRenderer,)
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class TripDetailsAPIView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (TripRenderer,)
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


# Location
class LocationListAPIView(ListCreateAPIView):
    renderer_classes = (TripRenderer,)
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerLocation,)

    def perform_create(self, serializer):
        trip = Trip.objects.all().get(id=self.kwargs["trip"])
        return serializer.save(trip=trip)

    def get_queryset(self):
        return self.queryset.filter(trip__id=self.kwargs["trip"], trip__created_by=self.request.user)


class LocationDetailsAPIView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (TripRenderer,)
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerLocation,)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(trip__created_by=self.request.user)


# DayPlace
class DayPlaceListAPIView(ListCreateAPIView):
    renderer_classes = (TripRenderer,)
    serializer_class = DayPlaceSerializer
    queryset = DayPlace.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerPlace,)

    def perform_create(self, serializer):
        location = Location.objects.all().get(id=self.kwargs["location"])
        return serializer.save(location=location)

    def get_queryset(self):
        return self.queryset.filter(location_id=self.kwargs["location"], location__trip__created_by=self.request.user)


class DayPlaceDetailsAPIView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (TripRenderer,)
    serializer_class = DayPlaceSerializer
    queryset = DayPlace.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerPlace,)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(location__trip__created_by=self.request.user)


class GetLocationByGoogleAPIView(APIView):
    def get(self, request):
        inp = request.query_params.get('input')
        res = requests.get("https://maps.googleapis.com/maps/api/place/autocomplete/json"
                     f"?input={inp}"
                     "&types=geocode"
                     "&key=")
        js = json.loads(res.text)
        print(js)
        return Response({'data': js})


class ImportAPIView(APIView):
    serializer_class = ImportSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[openapi.Parameter(name="file",in_=openapi.IN_FORM,type=openapi.TYPE_FILE,required=True,description="Document")])
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'INV_FILE'
                }, status=status.HTTP_400_BAD_REQUEST)
            print('YESS')
            excel_file = data.get('file')
            sheets_dict = pd.read_excel(excel_file, sheet_name=None)

            to_create = []
            trip_name = ""
            trip_date = ""
            for ind, sheet in enumerate(sheets_dict):
                for index, row in sheets_dict[sheet].iterrows():
                    col1 = row['col1']
                    col2 = row['col2']
                    col3 = row['col3']
                    if index == 0:
                        to_create.append({'location': {'name': col1, 'place_id': col2}, 'places': []})
                    elif index == 1:
                        if ind == 0:
                            trip_name = col1
                            trip_date = col2
                    else:
                        to_create[ind]['places'].append({'name': col1, 'visited': col2, 'sort_id': col3})
            print(to_create)
            if not trip_name:
                trip_name = "New trip"
            t = Trip(name=trip_name, created_by=request.user, start_date=trip_date)
            t.save()
            for ind, loc in enumerate(to_create):
                locat = Location(name=loc['location']['name'], place_id=loc['location']['place_id'], trip=t)
                locat.save()
                for place in loc['places']:
                    pl = DayPlace(name=place['name'], visited=place['visited'], sort_id=place['sort_id'], location=locat)
                    pl.save()


            return Response({
                'status': True,
                'message': 'SUCC',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'ERR',
            }, status=status.HTTP_400_BAD_REQUEST)



class ExportAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, tid):
        try:
            trip = Trip.objects.get(id=tid)
            locations = Location.objects.filter(trip__id=tid).values()
            dfs = []
            for loc in locations:
                places = DayPlace.objects.filter(location_id=loc['id']).values()
                d = {'col1': [loc['name'], trip.name] + [p['name'] for p in places], 'col2': [loc['place_id'], trip.start_date] + [p['visited'] for p in places],
                     'col3': ['', ''] + [p['sort_id'] for p in places]}
                df = pd.DataFrame(data=d)
                dfs.append(df)
            # df = pd.DataFrame.from_records(locations.vales())
            # df.to_excel(trip.name, index=False)

            io = BytesIO()

            writer = ExcelWriter(io)
            for i, d in enumerate(dfs):
                d.to_excel(writer, sheet_name=f'S{i}', index=False)

            writer.close()
            rFile = io.getvalue()
            response = HttpResponse(rFile, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=temp.xls'

            return response
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'ERR',
            }, status=status.HTTP_400_BAD_REQUEST)
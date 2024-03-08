from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TripSerializer
from .models import Trip
from rest_framework import permissions
from .permissions import IsOwner


class TripListAPIView(ListCreateAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class TripDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'id'



    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

from django.urls import path
from . import views


urlpatterns = [
    path('single-trip-summary/<int:tid>', views.TripSummaryStats.as_view(), name='single-trip-summary'),
    path('all-trip-summary', views.AllTripsSummaryStats.as_view(), name='all-trip-summary'),
]

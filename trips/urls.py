from django.urls import path
from . import views


urlpatterns = [
    path('', views.TripListAPIView.as_view(), name='trip-list'),
    path('<int:id>', views.TripDetailsAPIView.as_view(), name='trip-details'),
    path('locations-for-trip/<trip>', views.LocationListAPIView.as_view(), name='location-list'),
    path('location-by-id/<int:id>', views.LocationDetailsAPIView.as_view(), name='location-details'),
    path('places-for-location/<location>', views.DayPlaceListAPIView.as_view(), name='places-list'),
    path('place-by-id/<int:id>', views.DayPlaceDetailsAPIView.as_view(), name='place-details'),
    path('get-location-api', views.GetLocationByGoogleAPIView.as_view(), name='location-api'),

    path('import-trip', views.ImportAPIView.as_view(), name='import-trip'),
    path('export-trip/<int:tid>', views.ExportAPIView.as_view(), name='export-trip'),
]

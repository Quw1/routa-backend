from django.urls import path
from . import views


urlpatterns = [
    path('', views.TripListAPIView.as_view(), name='trips'),
    path('<int:id>', views.TripDetailsAPIView.as_view(), name='expense'),
]

from django.urls import path

from measurement.views import SensorView, MeasurementView, SensorRetrieve

urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('measurements/', MeasurementView.as_view()),
    path('sensors/<pk>/', SensorRetrieve.as_view()),
]

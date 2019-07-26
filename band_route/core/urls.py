from django.urls import path

from .views import FastestRouteAPIView

app_name = "core"
urlpatterns = [path("route", FastestRouteAPIView.as_view(), name="core-route")]

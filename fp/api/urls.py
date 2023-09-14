from django.urls import path

from .views import DocketView

app_name = 'api'
urlpatterns = [
    path('dockets/', DocketView.as_view(), name="dockets")
]
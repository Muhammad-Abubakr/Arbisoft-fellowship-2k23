from django.urls import path

from .views import DocketView, DocumentView

app_name = 'api'
urlpatterns = [
    path('dockets/', DocketView.as_view(), name="dockets"),
    path('documents/', DocumentView.as_view(), name="documents")
]
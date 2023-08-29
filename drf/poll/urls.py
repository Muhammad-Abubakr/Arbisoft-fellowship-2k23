from django.urls import path

from . import views

app_name = 'poll'
urlpatterns = [
    path('', views.IndexView.as_view(), name='questions'),
    path('<int:question_id>/', views.ChoiceView.as_view(), name='choices'),
    path('<int:question_id>/vote', views.VoteView.as_view(), name='vote')
]
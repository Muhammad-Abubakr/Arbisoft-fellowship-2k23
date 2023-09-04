from django.urls import include, path

from . import views

app_name = 'poll'
urlpatterns = [
    path('', views.IndexView.as_view(), name='questions'),
    path('<int:question_id>/', views.ChoiceView.as_view(), name='choices'),
    path('users/', views.UserList.as_view(), name="users"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('realtime/', views.realtime, name='realtime'),
    path('forecast/', views.forecast, name='forecast'),
    path('history/', views.history, name='history'),
    path('suggest_cities/', views.suggest_cities, name='suggest_cities')
]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.realtime),
# ]

from django.urls import path
from . import views
urlpatterns = [
    path('', views.homePage, name='home'),
    path('about/', views.aboutUs, name='about'),
    path('forecast/', views.forecast, name='forecast'),
    path('history/', views.history, name='history'),
    path('realtime/', views.realtime, name='realtime'),
    path('suggest_cities/', views.suggest_cities, name='suggest_cities'),
]

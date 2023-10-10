from django.urls import path
from . import views

app_name = 'aisweb'

urlpatterns = [
    path('', views.home, name='home'),
    path('aerodrome/', views.get_aerodrome_info, name='aerodrome'),
]

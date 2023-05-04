from django.urls import path
from api.devices import views

urlpatterns = [
    path('get/', views.get_getdevice, name='get'),
   
]

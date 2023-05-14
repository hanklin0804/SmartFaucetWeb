from django.urls import path, include
from api.devices import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'rpi/tap', views.TapViewSet)
router.register(r'rpi', views.RpiViewSet)


urlpatterns = [
    path('', include(router.urls))
]

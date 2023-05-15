from django.urls import path, include
from api.devices import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'tap', views.TapViewSet, basename='tap')
router.register(r'rpi', views.RpiViewSet)
# router.register(r'rpi/tap/<int:pk>/', views.TapViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls))
]

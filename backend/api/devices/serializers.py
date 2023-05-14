from rest_framework import serializers
from api.devices.models import RpiModel, TapModel


class RpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpiModel
        fields = '__all__'
        # read_only_fields = ['rpi_ip']
        
        
class TapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TapModel
        # fields = '__all__'
        exclude = ['device_id']
        # fields = [''device_id']
        # exclude = ['rpi_ip']

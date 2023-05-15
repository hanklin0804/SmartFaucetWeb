from rest_framework import serializers
from api.devices.models import RpiModel, TapModel


# class RpiSerializer(serializers.ModelSerializer):
#     # taps = serializers.Relat
#     class Meta:
#         model = RpiModel
#         fields = '__all__'
#         # read_only_fields = ['rpi_ip']
        
        
# class TapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TapModel
#         # fields = '__all__'
#         exclude = ['device_id']
#         # fields = [''device_id']
#         # exclude = ['rpi_ip']


from rest_framework import serializers
from api.devices.models import RpiModel, TapModel


class TapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TapModel
        # fields = '__all__'
        exclude = ['device_id']
        # fields = [''device_id']
        # exclude = ['rpi_ip']


class RpiSerializer(serializers.ModelSerializer):
    taps = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name = 'tap-detail')
    class Meta:
        model = RpiModel
        fields = '__all__'
        # read_only_fields = ['rpi_ip']


class RpiTapSerializer(serializers.ModelSerializer):
    taps = TapSerializer(many=True)
    class Meta:
        model = RpiModel
        fields = '__all__'
        # read_only_fields = ['rpi_ip']
        

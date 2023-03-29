from django.db import models
import uuid
from account.models import AccountProfileModel 
class AreaModel(models.Model):
    account_id = models.ForeignKey(AccountProfileModel, on_delete=models.CASCADE)
    device_area = models.CharField(max_length=100, unique=True)

class DeviceModel(models.Model):
    device_area = models.ForeignKey(AreaModel, on_delete=models.CASCADE)
    device_id = models.UUIDField(default=uuid.uuid4, editable=False)

class DeviceUpdateModel(models.Model):
    device_id = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    device_rt_switch =models.CharField(max_length=100)
    device_rt_interval = models.CharField(max_length=100)
    device_rt_conservation = models.CharField(max_length=100)
    device_mode = models.CharField(max_length=100)
    device_shutoff = models.CharField(max_length=100)
    device_interval = models.CharField(max_length=100)
    device_delay = models.CharField(max_length=100)
    device_distance = models.CharField(max_length=100)
    device_hygieneflush = models.CharField(max_length=100)
    device_defaultsetting =models.CharField(max_length=100)
    device_information = models.CharField(max_length=100)
    

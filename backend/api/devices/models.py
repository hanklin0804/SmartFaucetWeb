from django.db import models


class RpiModel(models.Model):
    rpi_ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    rpi_name = models.CharField(max_length=30, blank=True, null=True)
    rpi_location = models.CharField(max_length=30, blank=True, null=True)
    # ip = models.IPAddressField()
    # rpi_name = models.CharField(max_length=15)
    # real_address = models.CharField(max_length=30)
    class Meta:
        db_table = 'device_rpi_table'


class TapModel(models.Model):
    rpi = models.ForeignKey(RpiModel,related_name='taps', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=30)
    device_model = models.CharField(max_length=30)
    device_sn = models.CharField(max_length=30)
    device_id = models.CharField(max_length=30)
    fw_version = models.CharField(max_length=30)
    acc_amount = models.IntegerField(default=0)
    acc_feed_count = models.IntegerField(default=0)
    acc_feed_time = models.IntegerField(default=0)
    leak_info = models.CharField(max_length=30)

    # location = models.CharField(max_length=30, blank=True, null=True)

    # TODO
    # view 
    # 1. 檢視關於裝置資訊
    # 2. 資料庫更新關於裝置資訊
    # 3. 修改關於裝置資訊?
    # 4. 控制
    # 5. 檢視控制設定
    # 6. 修改控制設定

    # 當需要控制時才用到的欄位
    # 1.other model: use diff serializer 
    # 2.same model: use diff serializer  
    ir_duty = models.PositiveIntegerField(default=1) # 1~65535
    ir_range = models.PositiveSmallIntegerField(default=30) # 30~600
    self_preserver = models.PositiveIntegerField(default=1) #1~65535
    sen_feed = models.PositiveIntegerField(default=1) # 1~65535
    sen_stop = models.PositiveIntegerField(default=1) # 1~65535
    power_save = models.IntegerField(default=-1) # -1, 1~65535
    sol_time = models.PositiveIntegerField(default=30) # 30~65535
    feed_time_on1 = models.SmallIntegerField(default=-1) # -1, 0~2400
    feed_time_on2 = models.SmallIntegerField(default=-1) # -1, 0~2400
    feed_time_on3 = models.SmallIntegerField(default=-1) # -1, 0~2400
    feed_time_off1 = models.SmallIntegerField(default=-1) # -1, 0~2400
    feed_time_off2 = models.SmallIntegerField(default=-1) # -1, 0~2400
    feed_time_off3 = models.SmallIntegerField(default=-1) # -1, 0~2400
    amount_unit = models.BooleanField(default=True) # 0, 1
    feed_limit = models.BigIntegerField(default=-1) # -1, 1~4294967295
    amount_limit = models.IntegerField(default=-1) # -1, 1~65535
    
    batt_warn = models.SmallIntegerField(default=-1) # -1, 10~65
    batt_fail = models.SmallIntegerField(default=-1) # -1, 10~65
    leak_det_period = models.IntegerField(default=-1) # -1, 1~65535
    leak_det_keep = models.IntegerField(default=-1) # -1, 1~65535
    leak_det_ontime = models.SmallIntegerField(default=-1) # -1, 0~2400
    leak_det_offtime = models.SmallIntegerField(default=-1) # -1, 0~2400
    report_auto = models.CharField(max_length=15, default=-1) # -1, ip
    update_auto = models.SmallIntegerField(default=-1) # -1, 1
    

    # uuid = models.IntegerField(max_length=30)
    # private_ip = models.
    # public_ip = models.CharField(max_length=)
    # group = models.CharField(max_length=100)

    # ipv4 = models.GenericIPAddressField(protocol='IPv4')
    # ipv6 = models.GenericIPAddressField()
    # mac = 
    # userdwater = 
    # usedfeedcnt = 
    # accfeedtime = 
    # ip = models.IPAddressField()
    # rpi_name = models.CharField(max_length=15)
    # real_address = models.CharField(max_length=30)
    # model.case

    class Meta:
        db_table = 'device_rpi_tap_table'
        # verbose_name = 'device'
        # verbode_name_plural = 'devices'


class WeekStatisticsModel(models.Model):
    tap = models.ForeignKey(TapModel,related_name='week', on_delete=models.CASCADE)
    time = models.DateTimeField()
    amount = models.IntegerField()
    feed_count = models.IntegerField()
    feed_time = models.IntegerField()
    class Meta:
        db_table = 'statistics_week'

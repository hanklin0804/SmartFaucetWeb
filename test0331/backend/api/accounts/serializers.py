from rest_framework import serializers
from api.accounts.models import AccountModel
# from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        # must need password ? 
        fields = ('account', 'password',  'email', 'name', 'phone', 'company', 'information', 'is_active', 'is_staff')
        # extra_kwargs = {'password': {'write_only': True}}
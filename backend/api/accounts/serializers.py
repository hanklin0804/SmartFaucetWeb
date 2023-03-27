from rest_framework import serializers
from accounts.models import AccountModel


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel 
        fields = ('account', 'password',  'email', 'name', 'phone', 'company', 'information', 'is_active', 'is_staff')
        # extra_kwargs = {'password': {'write_only': True}}
  
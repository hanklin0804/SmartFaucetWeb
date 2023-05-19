from rest_framework import serializers
from api.accounts.models import AccountModel
# from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        # must need password ? 
        # fields = 。'__all__'
        fields = ('account', 'password',  'email', 'name', 'phone', 'company', 'information', 'is_active', 'is_staff') #, 'is_active', 'is_staff'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_active': {'write_only': True}
        }
        

# # can see, can update
# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccountModel
#         fields = ('account','email', 'name', 'phone', 'company', 'information') 
#         # extra_kwargs = {'password': {'write_only': True}}
#         # write_only_fields = ['is_active', 'is_staff', 'password']
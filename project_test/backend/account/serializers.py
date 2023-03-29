from rest_framework import serializers
from account.models import AccountModel
# from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        # must need password ? 
        fields = ('account', 'password',  'email', 'name', 'phone', 'company', 'information', 'is_active', 'is_staff')
        # extra_kwargs = {'password': {'write_only': True}}
    # def create(seld, validated_data):
    #     password = validated_data.pop('password')
    #     user = AccountModel(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user

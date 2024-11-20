from rest_framework import serializers
from deposits.models import *


class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit',)


class DepositSerializer(serializers.ModelSerializer):
    depositoption_set = DepositOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('contract_user',)


class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving',)


class SavingSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Saving
        fields = '__all__'
        read_only_fields = ('contract_user',)
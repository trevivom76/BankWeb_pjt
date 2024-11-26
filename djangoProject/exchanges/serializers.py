from rest_framework import serializers
from exchanges.models import *

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'